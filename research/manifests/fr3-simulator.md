# Franka Research 3 simulator asset provenance

Verified 2026-11-13 for the original foundation problem `fr3-joint-interpolation`. This is an asset/implementation manifest, not a new paper or a claim to reproduce a research result.

## Primary sources

- [Official MuJoCo Menagerie FR3 package](https://github.com/google-deepmind/mujoco_menagerie/tree/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3).
- [Pinned package README](https://github.com/google-deepmind/mujoco_menagerie/blob/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3/README.md) identifies the robot as Franka Research 3 and describes conversion from the manufacturer description. It is a simplified simulation model, not Panda renamed to FR3.
- [Pinned full LICENSE](https://github.com/google-deepmind/mujoco_menagerie/blob/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3/LICENSE): Apache-2.0 plus an appended BSD notice. Preserve the complete file and upstream attribution when distributing the model; do not drop the appended notice.
- [Franka manufacturer simulation directory](https://franka.de/models-and-simulation) links FR3 users to MuJoCo Menagerie.
- [Franka control-interface specifications](https://frankarobotics.github.io/docs/robot_specifications.html) provide current hardware joint limits. This exercise uses the exact pinned model ranges, rather than assuming every firmware/model generation is interchangeable.
- [MuJoCo forward computation](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-forward) and [Python rendering API](https://mujoco.readthedocs.io/en/stable/python.html) document the simulator-side operations.

## Pin and integrity

Repository: `google-deepmind/mujoco_menagerie`; directory: `franka_fr3`; commit: `98a70c569c4c1b6da467a20012f766ee1f8dc521`.

`apps/simulator/assets.lock.json` lists every downloaded file with expected bytes and SHA-256. The lock contains 47 files; its SHA-256 is `c5d2f7f786b6dad4b449398fb7c67157b2e7496b7f6ceef246c03cecf21cf23d`. The setup helper downloads only those pinned upstream paths into ignored `.local/simulator/franka_fr3/`. It validates bytes/hash; no image is copied from a paper.

| Artifact | SHA-256 |
|---|---|
| fr3.xml | `8a2d8fdc9dd73b1226ca34de5517e7c7eb08b850b68c3d36d9e93b1b183b9b86` |
| scene.xml | `8f17f883872d6c95b63239bd82ca4374771deca9949b8fc9577356209f662ebe` |
| LICENSE | `5e15554a918bf661583d7df7a1014177be4fed561532aaaee852dca06c71821a` |
| README.md | `19c8ad2e78fb0d046bd9db23a64448a81f046d5b4fe0bdd0eeebeec6759fab41` |

The curator independently verified all 47 cached file sizes/hashes and byte-compared those four identity/license/model files against their pinned primary-source URLs. Parsed MJCF model name is `fr3`; it declares the seven named FR3 joints and exactly the ranges below.

## Physical contract

No gripper is mounted. The displayed attachment frame is `attachment_site`, at `[0,0,0.107]` meters relative to `fr3_link7`. World and base coincide; +z is up. Joint coordinates are radians, ordered `fr3_joint1` through `fr3_joint7`, with right-hand positive rotation about each joint-local +z axis.

| Joint | Minimum rad | Maximum rad |
|---|---:|---:|
| 1 | -2.9007 | 2.9007 |
| 2 | -1.8361 | 1.8361 |
| 3 | -2.9007 | 2.9007 |
| 4 | -3.0770 | -0.1169 |
| 5 | -2.8763 | 2.8763 |
| 6 | 0.4398 | 4.6216 |
| 7 | -3.0508 | 3.0508 |

Reset follows the upstream home key exactly: `[0,0,0,-1.57079,0,1.57079,-0.7853]`. Original public goal: `[0.4,-0.3,0.2,-1.8,0.1,1.9,-0.4]`. The learner returns 41 demonstration samples with both endpoints. Fixture license: CC0-1.0 for these original numerical exercises; upstream meshes retain their own license.

## Runtime and scope

MuJoCo3.3.7, NumPy2.2.4 and Pillow11.2.1 are pinned by `apps/simulator/requirements.txt`, including dependency versions. Simulator seed is 0; timestep0.002s, implicitfast integrator, Newton solver, 100iterations, tolerance1e-8. Each frame resets state, writes seven qpos values and calls `mj_forward`; **zero dynamics steps** are executed. The timing parameters are pinned for provenance, not claims of physical execution.

The separate loopback process accepts only bounded joint vectors, not learner source, model paths, URLs or scripts. The browser receives a bounded 640x480 rendered PNG and numerical pose. Its code/simulation switch does not put native simulation inside the learner evaluator. Render success does not establish collision clearance or real-robot safety.

## Implementable progression

1. [Interpolate Franka FR3 Joint Waypoints](../../content/problems/fr3-joint-interpolation/blueprint.md): the current original foundation exercise and optional kinematic replay.
2. Future candidates, not yet published by this manifest: compare joint interpolation against Cartesian paths; check joint velocity under an explicit duration; compute a geometric Jacobian; solve bounded damped-least-squares IK; assess collision and control constraints before dynamics execution.

The task's mathematical explanation and grading are independent of rendering. A missing MuJoCo runtime is a preview availability error, not a failed numerical solution.
