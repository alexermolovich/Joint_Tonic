# Franka Research 3 in the local workspace

Open `/problems/fr3-joint-interpolation`. The page requests a MuJoCo frame immediately, lazily creating the native model on first use. Switch between **Code** and **Simulation** in the right pane; Theory stays on the left and the editor remains mounted. The reference solution is prefilled for new/untouched drafts; Reset code restores the starter. Select Simulation and press Run and play to evaluate the current editor and automatically replay the actual function output on the public example. Existing fresh results use Play your result. Editing code stops playback and requires Run and play again, so stale results are not mistaken for the current function. Expand Function inputs and returned joint positions to inspect the exact arguments and selected returned row. The Simulation tab streams live frames. Drag with mouse/touch to orbit, scroll to zoom, or focus the view and use arrow keys, +/− and R. Reset camera changes only the viewpoint; Reset robot returns the arm home. You can also select individual waypoints.

This is the actual Franka Research 3 model from MuJoCo Menagerie, not the Panda model. The upstream revision, licenses and all 47 file hashes are in `apps/simulator/assets.lock.json` and `research/manifests/fr3-simulator.md`. Assets are downloaded into ignored `.local/simulator/franka_fr3`; no download occurs when a learner opens the problem.

## Setup

The existing Windows development setup uses WSL and `/home/alex/.venvs/joint-tonic/bin/python`. From the repository in PowerShell:

```powershell
wsl.exe --cd /mnt/c/Users/101199420/Documents/ChatGPT/Joint_Tonic --exec /home/alex/.venvs/joint-tonic/bin/python -m pip install -r apps/simulator/requirements.txt
wsl.exe --cd /mnt/c/Users/101199420/Documents/ChatGPT/Joint_Tonic --exec /home/alex/.venvs/joint-tonic/bin/python apps/simulator/setup_assets.py
npm run dev
```

For Linux, use the project Python environment:

```sh
python -m pip install -r apps/simulator/requirements.txt
python apps/simulator/setup_assets.py
JOINT_TONIC_PYTHON=/path/to/project/python npm run dev
```

`npm run dev` starts web 3000, evaluator 8765 and simulator 8766. When the web server is already running, start just the simulator from the repository using the same Python environment:

```sh
python -u apps/simulator/server.py
```

MuJoCo 3.3.7 and its Python dependencies are pinned. Linux defaults to offscreen EGL, using the machine's graphics/Mesa runtime. Native Windows rendering is not the verified baseline. The local baseline uses no external desktop window: the MuJoCo image is embedded inside the coding pane. If the renderer cannot initialize, check the simulator stderr, graphics runtime and asset hashes; the UI provides Retry and ordinary coding remains available.

## Data and execution contract

- `POST /api/simulator/fr3` proxies to loopback `POST /v1/fr3/frame`. `{}` asks for home; `{ "q": [seven joint angles] }` asks for a pose. An optional `camera` object accepts azimuth in [-360,360] degrees, elevation in [-85,85] degrees and distance in [0.5,4] metres. No code, paths or arbitrary models are accepted.
- Requests are bounded to 2048 bytes. The service validates finite values and exact model joint limits. One 640×480 PNG plus joint/tool state is returned; rendering is serialized to preserve the native GL context.
- The browser keeps one request in flight and coalesces control changes into the next frame; hidden views stop live requests and hidden browser tabs pause rendering. The proxy times out after 30 seconds. A native renderer hang may require restarting the separate simulator process; this is not a hardened public renderer deployment.
- `mj_forward` computes kinematics at each requested configuration. No dynamics steps are taken; no collision-free path, torque tracking or hardware safety is certified. MuJoCo's attachment_site is the reported tool frame in the world/FR3-base frame, with position in metres. The frame is not an added gripper fingertip.
- The isolated evaluator copies the problem's authored `preview.py` into the disposable sandbox. It evaluates the fixed public fixture, returns bounded numerical waypoints, and never gives learner code access to the simulator process. Both the worker transport and simulator validate the angles independently. Preview failure does not itself change a correct grading verdict.
- The preview uses the evaluated code snapshot, with a stale-draft notice after edits. No reference animation substitutes for failed learner output. Playback is user-triggered and uses a display clock; slow rendering can skip visible samples. It is not real-time robot control; static waypoint selection supplies a nonanimated alternative.
- Job lineage includes the harness and preview hashes. Frames identify the pinned MuJoCo version, asset commit/hash and correlation ID. Local workspace ownership remains the existing prototype contract; this does not make simulator/evaluator endpoints suitable for public hosted traffic.

## Focused checks

Use `npm run typecheck`, `npm run validate`, `python apps/simulator/test_simulator.py`, `python tests/robot-preview-checks.py`, `node --test tests/fr3-ui.test.mjs`, and `python apps/worker/check_references.py --sandbox fr3-joint-interpolation`. Browser checks should cover initialization on open, Code/Simulation switches without lost edits, valid learner replay, invalid-output/offline states, keyboard tabs and narrow layouts. The public and hidden grading cases remain numerical; rendered pixels are explanatory feedback.
