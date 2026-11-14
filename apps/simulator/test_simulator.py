"""Focused actual-MuJoCo + local HTTP contract checks. Run in simulator Python env."""
import base64
import io
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image

from server import GOAL, HOME, LIMITS, DEFAULT_CAMERA, Handler, Renderer, SimulatorServer, validate_request, validate_camera


class InputContract(unittest.TestCase):
    def test_camera_bounds(self):
        self.assertEqual(validate_camera(DEFAULT_CAMERA), DEFAULT_CAMERA)
        for camera in [None, [], {}, {**DEFAULT_CAMERA, "path": "model.xml"},
                       {**DEFAULT_CAMERA, "azimuth": True}, {**DEFAULT_CAMERA, "distance": .49},
                       {**DEFAULT_CAMERA, "elevation": 86}, {**DEFAULT_CAMERA, "azimuth": 361},
                       {**DEFAULT_CAMERA, "distance": float("nan")}, {**DEFAULT_CAMERA, "distance": 10**1000}]:
            with self.subTest(camera=camera), self.assertRaises(ValueError):
                validate_camera(camera)
    def test_home_and_limits(self):
        self.assertEqual(validate_request({}), HOME)
        self.assertEqual(validate_request({"q": GOAL}), GOAL)
        for column in (0, 1):
            self.assertEqual(validate_request({"q": [r[column] for r in LIMITS]}), [r[column] for r in LIMITS])

    def test_invalid_boundary(self):
        invalid = [None, [], {"code": "pass"}, {"q": []}, {"q": HOME + [0]},
                   {"q": [True] + HOME[1:]}, {"q": ["0"] + HOME[1:]},
                   {"q": [float("nan")] + HOME[1:]}, {"q": [float("inf")] + HOME[1:]},
                   {"q": [3] + HOME[1:]}]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_request(value)


class NativeMuJoCo(unittest.TestCase):
    def test_pinned_fr3_render_and_forward_kinematics(self):
        renderer = Renderer()
        try:
            home = renderer.frame(HOME)
            goal = renderer.frame(GOAL)
            again = renderer.frame(HOME)
            np.testing.assert_allclose(home["tool_position_m"], [0.5544994780317353, 0, 0.6245024294875894], atol=1e-10)
            np.testing.assert_array_equal(home["tool_position_m"], again["tool_position_m"])
            rotation = np.array(home["tool_rotation"])
            np.testing.assert_allclose(rotation.T @ rotation, np.eye(3), atol=1e-12)
            self.assertAlmostEqual(np.linalg.det(rotation), 1.0)
            self.assertGreater(np.linalg.norm(np.array(home["tool_position_m"]) - goal["tool_position_m"]), 0.01)
            self.assertEqual(home["asset_commit"], "98a70c569c4c1b6da467a20012f766ee1f8dc521")
            self.assertEqual(home["physics_steps"], 0)
            image = Image.open(io.BytesIO(base64.b64decode(home["image_png_base64"])))
            self.assertEqual(image.size, (640, 480))
            self.assertGreater(np.asarray(image).std(), 10)
            self.assertNotEqual(home["image_png_base64"], goal["image_png_base64"])
            orbit = renderer.frame(HOME, {"azimuth": 45, "elevation": -40, "distance": 1.3})
            self.assertNotEqual(home["image_png_base64"], orbit["image_png_base64"])
            np.testing.assert_array_equal(home["tool_position_m"], orbit["tool_position_m"])
            reset = renderer.frame(HOME)
            self.assertEqual(reset["camera"], DEFAULT_CAMERA)
            reset_image = np.asarray(Image.open(io.BytesIO(base64.b64decode(reset["image_png_base64"])))).astype(float)
            self.assertLess(np.abs(reset_image - np.asarray(image).astype(float)).mean(), 1.0)
        finally:
            renderer.close()


class HttpBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = SimulatorServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, path, payload=None, headers=None):
        request = Request(self.url + path, data=payload, headers=headers or {})
        try:
            response = urlopen(request, timeout=10)
        except HTTPError as error:
            response = error
        return response.status, json.load(response), response.headers

    def test_lazy_health(self):
        correlation = "44444444-4444-4444-8444-444444444444"
        status, body, headers = self.request("/health", headers={"X-Correlation-Id": correlation})
        self.assertEqual(status, 200)
        self.assertFalse(body["scene_loaded"])
        self.assertEqual(headers["X-Correlation-Id"], correlation)

    def test_origin_host_and_content_type(self):
        for headers, status in [({"Origin": "https://evil.example", "Content-Type": "application/json"}, 403),
                                ({"Host": "evil.example", "Content-Type": "application/json"}, 403),
                                ({"Content-Type": "text/plain"}, 415)]:
            self.assertEqual(self.request("/v1/fr3/frame", b"{}", headers)[0], status)

    def test_bounded_invalid_payloads(self):
        headers = {"Content-Type": "application/json"}
        for payload, status in [(b"x" * 2049, 413), (b"{", 400), (b'{"q":[0]}', 400), (b'{"asset":"arbitrary.xml"}', 400)]:
            self.assertEqual(self.request("/v1/fr3/frame", payload, headers)[0], status)
        self.assertIsNone(self.server.renderer)


if __name__ == "__main__":
    unittest.main()
