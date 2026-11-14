"""Loopback-only, bounded MuJoCo forward-kinematics renderer. No learner code."""
import base64
import hashlib
import hmac
import io
import json
import math
import os
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

from setup_assets import ASSET_DIR, LOCK_PATH, verify_assets

# EGL uses WSL/Linux offscreen rendering; native Windows uses MuJoCo's GLFW default.
if sys.platform == "linux":
    os.environ.setdefault("MUJOCO_GL", "egl")

PROTOCOL = "joint-tonic.simulator.v1"
VERSION = "3.3.7"
WIDTH, HEIGHT = 640, 480
LIMITS = [[-2.9007, 2.9007], [-1.8361, 1.8361], [-2.9007, 2.9007],
          [-3.0770, -0.1169], [-2.8763, 2.8763], [0.4398, 4.6216], [-3.0508, 3.0508]]
HOME = [0.0, 0.0, 0.0, -1.57079, 0.0, 1.57079, -0.7853]
GOAL = [0.4, -0.3, 0.2, -1.8, 0.1, 1.9, -0.4]
DEFAULT_CAMERA = {"azimuth": 135.0, "elevation": -24.0, "distance": 1.8}


def validate_camera(camera):
    if not isinstance(camera, dict) or set(camera) != set(DEFAULT_CAMERA):
        raise ValueError("Camera requires azimuth, elevation and distance")
    for key, low, high in (("azimuth", -360, 360), ("elevation", -85, 85), ("distance", .5, 4.0)):
        value = camera[key]
        if type(value) not in (int, float) or not low <= value <= high or not math.isfinite(value):
            raise ValueError("Camera values must be finite and within the orbit bounds")
    return {key: float(camera[key]) for key in DEFAULT_CAMERA}


def validate_request(payload):
    if not isinstance(payload, dict) or set(payload) - {"q", "camera"}:
        raise ValueError("Expected optional q and camera")
    validate_camera(payload.get("camera", DEFAULT_CAMERA))
    q = payload.get("q", HOME)
    if not isinstance(q, list) or len(q) != 7:
        raise ValueError("q must contain exactly seven joint angles in radians")
    for index, value in enumerate(q):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Each joint angle must be a finite number")
        if not math.isfinite(value) or not LIMITS[index][0] <= value <= LIMITS[index][1]:
            raise ValueError(f"Joint {index + 1} is outside the FR3 position limits")
    return [float(value) for value in q]


class Renderer:
    def __init__(self):
        import mujoco
        from PIL import Image
        if mujoco.__version__ != VERSION:
            raise RuntimeError(f"Expected MuJoCo {VERSION}; install apps/simulator/requirements.txt")
        self.lock = verify_assets()
        self.mujoco, self.Image = mujoco, Image
        self.model = mujoco.MjModel.from_xml_path(str(ASSET_DIR / "scene.xml"))
        self.model.opt.timestep = 0.002
        self.model.opt.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
        self.model.opt.solver = mujoco.mjtSolver.mjSOL_NEWTON
        self.model.opt.iterations = 100
        self.model.opt.tolerance = 1e-8
        self.data = mujoco.MjData(self.model)
        self.joints = [self.model.joint(f"fr3_joint{i}") for i in range(1, 8)]
        for joint, limits in zip(self.joints, LIMITS):
            if list(joint.range) != limits:
                raise RuntimeError("Pinned FR3 joint limits differ from the learner contract")
        self.site = self.model.site("attachment_site").id
        self.renderer = mujoco.Renderer(self.model, height=HEIGHT, width=WIDTH)
        self.camera = mujoco.MjvCamera()
        self.camera.lookat[:] = [0.12, 0.0, 0.42]
        self.camera.distance, self.camera.azimuth, self.camera.elevation = 1.8, 135, -24
        self.options = mujoco.MjvOption()
        self.options.geomgroup[3] = 0  # Collision meshes remain in model, not drawn over visuals.

    def frame(self, q, camera=None):
        mujoco = self.mujoco
        camera = validate_camera(DEFAULT_CAMERA if camera is None else camera)
        self.camera.azimuth = camera["azimuth"]
        self.camera.elevation = camera["elevation"]
        self.camera.distance = camera["distance"]
        mujoco.mj_resetData(self.model, self.data)
        for joint, angle in zip(self.joints, q):
            self.data.qpos[joint.qposadr[0]] = angle
        self.data.ctrl[:] = q
        # A kinematic pose query, intentionally not dynamics or collision-free planning.
        mujoco.mj_forward(self.model, self.data)
        self.renderer.update_scene(self.data, camera=self.camera, scene_option=self.options)
        # Keep software rendering interactive: these affect appearance, never kinematics.
        self.renderer.scene.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = False
        self.renderer.scene.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = False
        rgb = self.renderer.render()
        image = io.BytesIO()
        self.Image.fromarray(rgb).save(image, format="PNG", compress_level=3)
        encoded = base64.b64encode(image.getvalue()).decode("ascii")
        if len(encoded) > 1_500_000:
            raise RuntimeError("Rendered frame exceeds bounded output")
        return {"protocol": PROTOCOL, "backend": "mujoco", "backend_version": VERSION,
                "model": "franka_fr3", "asset_commit": self.lock["commit"],
                "asset_manifest_sha256": hashlib.sha256(LOCK_PATH.read_bytes()).hexdigest(),
                "q": q, "home_q": HOME, "goal_q": GOAL, "camera": camera,
                "joint_limits_rad": LIMITS, "joint_names": [f"fr3_joint{i}" for i in range(1, 8)],
                "tool_position_m": self.data.site_xpos[self.site].tolist(),
                "tool_rotation": self.data.site_xmat[self.site].reshape(3, 3).tolist(),
                "tool_frame": "attachment_site", "reference_frame": "world (FR3 base)",
                "width": WIDTH, "height": HEIGHT, "image_png_base64": encoded,
                "capabilities": ["kinematic_pose", "rgb_frame", "orbit_camera"], "physics_steps": 0,
                "seed": 0, "timestep_s": 0.002}

    def close(self):
        self.renderer.close()


class SimulatorServer(HTTPServer):
    # Single-threaded server keeps the GL context on its creating thread and serializes renders.
    allow_reuse_address = True
    request_queue_size = 4
    renderer = None

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(5)
        return connection, address


class Handler(BaseHTTPRequestHandler):
    server_version = "JointTonicSimulator/1"

    def log_message(self, *_args):
        pass

    def correlation_id(self):
        try:
            return str(uuid.UUID(self.headers.get("X-Correlation-Id", "")))
        except (ValueError, AttributeError):
            return str(uuid.uuid4())

    def reply(self, status, data, correlation):
        encoded = json.dumps(data, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Correlation-Id", correlation)
        self.end_headers()
        self.wfile.write(encoded)

    def local_request(self):
        try:
            token = os.environ.get("SIMULATOR_SERVICE_TOKEN", "")
            if token:
                # An authenticated web proxy owns identity; no learner code enters this service.
                return len(token) >= 32 and hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + token)
            host = urlsplit("http://" + self.headers.get("Host", "")).hostname
            origin = self.headers.get("Origin")
            return host in {"localhost", "127.0.0.1", "::1"} and (not origin or origin in {
                "http://localhost:3000", "http://127.0.0.1:3000"})
        except ValueError:
            return False

    def do_GET(self):
        correlation = self.correlation_id()
        if not self.local_request():
            return self.reply(403, {"error": "Local requests only"}, correlation)
        if self.path != "/health":
            return self.reply(404, {"error": "Not found"}, correlation)
        return self.reply(200, {"protocol": PROTOCOL, "status": "ready", "scene_loaded": self.server.renderer is not None}, correlation)

    def do_POST(self):
        correlation = self.correlation_id()
        started = time.monotonic()
        status = 500
        try:
            if not self.local_request():
                status = 403
                return self.reply(status, {"error": "Local requests only"}, correlation)
            if self.path != "/v1/fr3/frame":
                status = 404
                return self.reply(status, {"error": "Not found"}, correlation)
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                status = 415
                return self.reply(status, {"error": "Expected application/json"}, correlation)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 2048:
                    status = 413
                    return self.reply(status, {"error": "Request must be 1..2048 bytes"}, correlation)
                payload = json.loads(self.rfile.read(length))
                q = validate_request(payload)
            except (ValueError, OverflowError, UnicodeDecodeError) as error:
                status = 400
                return self.reply(status, {"error": str(error)[:200]}, correlation)
            if self.server.renderer is None:
                self.server.renderer = Renderer()
            frame = self.server.renderer.frame(q, payload.get("camera"))
            frame["correlation_id"] = correlation
            status = 200
            self.reply(status, frame, correlation)
        except Exception as error:
            status = 503
            self.reply(status, {"error": "Simulator unavailable. Check the local simulator setup and restart it."}, correlation)
            print(json.dumps({"event": "simulator_failure", "correlation_id": correlation, "error_type": type(error).__name__}), flush=True)
        finally:
            print(json.dumps({"event": "simulator_frame", "correlation_id": correlation, "status": status,
                              "duration_ms": round((time.monotonic() - started) * 1000)}), flush=True)


if __name__ == "__main__":
    server = SimulatorServer(("127.0.0.1", 8766), Handler)
    print(json.dumps({"event": "simulator_listening", "host": "127.0.0.1", "port": 8766, "protocol": PROTOCOL}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if server.renderer:
            server.renderer.close()
        server.server_close()
