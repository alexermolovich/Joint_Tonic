# Local FR3 MuJoCo renderer

This trusted, separate process renders the actual **Franka Research 3 arm** using the Google DeepMind MuJoCo Menagerie model. It does not load or execute learner code. The FR3 has seven joints and no attached hand in this asset. `attachment_site` is the flange attachment frame, not a gripper tip.

## Setup

Use Python 3.12 and install the pinned renderer environment, then fetch its immutable assets:

```sh
python -m pip install -r apps/simulator/requirements.txt
python apps/simulator/setup_assets.py
python -u apps/simulator/server.py
```

For this Windows workspace, the tested backend is WSL Ubuntu with `/home/alex/.venvs/joint-tonic/bin/python`. Run from the repository's `/mnt/c/.../Joint_Tonic` path. Linux defaults to EGL offscreen rendering, including software rendering when a GPU is unavailable. Shadows and reflections are disabled for interactive software rendering; numerical kinematics are unaffected. A native Windows Python installation may use GLFW, but that renderer was not verified here. No visible desktop window is launched; the website displays bounded PNG frames inside its Simulation tab.

The setup helper downloads only 47 allowlisted files from pinned commit `98a70c569c4c1b6da467a20012f766ee1f8dc521` into ignored `.local/simulator/franka_fr3/` (~57 MB). Every file has a byte count and SHA-256 in `assets.lock.json`; startup verifies all hashes before loading XML. Asset downloading is a separate explicit setup operation, never a side effect of an HTTP request. Runtime rendering makes no network calls.

## Protocol v1

Listen only on `127.0.0.1:8766`. The web app calls its same-origin proxy; the service does not enable CORS. Host and Origin checks reject nonlocal browser callers. The serial server owns one renderer on one thread, eliminating GL-context races and per-browser native-process leaks. It starts with no scene: the first valid frame request loads the model. Each frame resets data and applies the supplied pose, so tabs/users cannot inherit another request's state.

- `GET /health`: liveness plus `scene_loaded`.
- `POST /v1/fr3/frame`, JSON `{}`: initialize and render the pinned home pose.
- `POST /v1/fr3/frame`, JSON `{"q":[seven numbers],"camera":{"azimuth":135,"elevation":-24,"distance":1.8}}`: render that configuration after finite/type/joint-limit validation. Camera is optional and validated: azimuth ±360°, elevation ±85°, distance0.5–4m. Defaults are restored on every request that omits camera, preventing cross-view camera leakage. Unknown fields, booleans, nested values, wrong lengths, and out-of-range joints are rejected.
- Input max 2048 bytes; connections time out after 5 seconds, queue depth 4; one 640×480 PNG per response with base64 capped at 1.5 MB. The control-plane fetch should time out after 15 seconds to allow first model load.
- Response includes protocol/backend version, asset commit/manifest hash, q, joint limits, home/goal, `tool_position_m`, 3×3 `tool_rotation`, reference/tool frames, PNG data, and correlation ID. Logs contain status, duration, and correlation ID, not learner source or credentials.
- Only `kinematic_pose` and `rgb_frame` capabilities are implemented. No dynamics step, arbitrary model upload, native-script execution, physical-robot control, or unrestricted renderer stream is exposed. A simulator error is HTTP503 and must not alter numerical grading.

The proxy timeout bounds how long the browser waits; it cannot interrupt a native renderer hang. Restart the separate simulator process after such a platform failure. Native-call supervision/resource termination is a remaining requirement before accepting public untrusted traffic. The local service accepts bounded numeric poses against one verified model, not learner programs.

The server resets qvel and state and calls `mj_forward`, not `mj_step`. Time is zero, seed 0 (no randomness), world/base is fixed with +z up, hinge values are radians, position is meters, and the rotation maps attachment-frame coordinates to world/base. MuJoCo version 3.3.7; timestep 0.002 s, implicitfast integrator, Newton solver, 100 iterations, tolerance1e-8 are pinned even though this kinematic slice integrates no physics. Contact geometries remain loaded; the replay is not a collision or torque safety certificate. Default orbit camera: lookat[0.12,0,0.42], distance1.8, azimuth135°, elevation−24°.

## Checks

```sh
python apps/simulator/test_simulator.py
```

Checks exercise invalid/oversized HTTP input and origin/host handling, lazy initialization, actual pinned FR3 model hashes/limits, home forward kinematics, deterministic reset, proper rotation, and nonempty different rendered images at two poses. They do not certify collision-free or dynamically feasible motion.

## Model provenance and notices

Primary source: [Menagerie FR3 at the pinned commit](https://github.com/google-deepmind/mujoco_menagerie/tree/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3). Its README identifies the model as the FR3 derived from the manufacturer's public robot description. The model's Apache-2.0 license also includes BSD attribution text; the complete upstream LICENSE, README, and mesh notices are retained unchanged by the downloader. Upstream assets are not copied into the public web directory. Rendered frames are produced locally from that licensed model. The manifest distinguishes this model from Menagerie's separate Franka Panda asset.
