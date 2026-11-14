# Curriculum authoring and implementation plan

The first release contains ten practical components. Each problem is a folder of reviewable Markdown, code, and deterministic tests. `MVP_10.md` is the implementation commitment; the root `CURRICULUM.md` remains the larger 189-problem roadmap.

The learning program mixes **robotics concepts** with **research-paper components**. A learner should practice what a coordinate frame, joint configuration, noisy sensor, map cell, controller state, or rollout outcome means before those objects appear inside a large model. Python syntax and general mathematics are assumed tools; they are not separate curriculum tracks. Mathematics is explained only where it clarifies a concrete robotics mechanism.

## First ten: the learning and assessment map

| # | Problem folder | Prior knowledge | Theory objective | Observable result |
|---:|---|---|---|---|
| 1 | [se3-transform-points](problems/se3-transform-points/problem.md) | Python arrays and matrix multiplication | Distinguish a point from its coordinate description; connect row batches to a column-vector rigid transform | New float64 world-frame points; correct single/batch/empty shapes; invalid rigid matrices rejected |
| 2 | [project-camera-points](problems/project-camera-points/problem.md) | Problem 1; division and masks | Explain perspective ratios, optical axes, pixel units, and independent geometric/image validity | Aligned pixel/depth/valid arrays; NaNs behind the camera; half-open image bounds |
| 3 | [box-iou-broadcast](problems/box-iou-broadcast/problem.md) | Array broadcasting | Derive continuous intersection/union and understand the two independent pair axes | Float64 N-by-M overlap matrix; zero-area and empty-set behavior; symmetric comparisons |
| 4 | [decode-yolo-grid](problems/decode-yolo-grid/problem.md) | Problems 2 and 3 | Map local cell coordinates to image rectangles and separate geometric decoding from confidence/NMS | Deterministically ordered per-class box records; clipping and inclusive score filtering |
| 5 | [class-aware-nms](problems/class-aware-nms/problem.md) | Problem 3; sorting and indices | Follow greedy selection, class isolation, strict threshold semantics, and original-index preservation | A stable list of surviving input indices; removed candidates cannot suppress others |
| 6 | [clip-symmetric-loss](problems/clip-symmetric-loss/problem.md) | Tensor normalization and cross-entropy | Explain diagonal pairing, in-batch negatives, temperature, and bidirectional retrieval | A differentiable scalar; correct numerical loss and finite gradients |
| 7 | [rt1-action-codec](problems/rt1-action-codec/problem.md) | Array broadcasting, floor, and clipping | Relate action bins to physical units, vocabulary IDs, reconstruction error, and saturation | Int64 token IDs plus float64 bin-center commands; shape and codec settings preserved |
| 8 | [diffusion-action-noising](problems/diffusion-action-noising/problem.md) | Tensor axes; square roots | Separate clean signal, supplied noise, cumulative schedule, per-batch timestep, and padding mask | Deterministic noised chunks and target noise; correct endpoints, masks, and gradients |
| 9 | [validate-robot-episodes](problems/validate-robot-episodes/problem.md) | Lists/dictionaries, shapes, and time | Treat physical metadata as a data contract; explain validation hierarchy and located diagnostics | Stable issue dictionaries with exact episode/path/code; schema errors distinguished from data anomalies |
| 10 | [edge-inference-release-gate](problems/edge-inference-release-gate/problem.md) | Means, quantiles, grouping | Separate accuracy, tail latency, sequential throughput, memory, slices, and missing evidence | Metrics by hardware plus every failed policy rule in deterministic order |

The geometry/perception path is `1 → 2`, `3 → 4`, and `3 → 5`, followed by a composed camera-to-detection discussion. Problems 6–8 form a second mechanism-focused path; Problems 9–10 connect these components to data and deployment evidence. Prerequisites guide learning without preventing direct access.

## Problem folder contract

```text
content/problems/<stable-slug>/
  blueprint.md   # authoring decisions, physical/runtime contract, evaluation plan
  meta.json      # typed catalog metadata, versions, paper IDs, prerequisites
  problem.md     # concise task, exact I/O and errors, constraints, basic examples
  theory.md      # original intuition, defined math, worked numbers, robot relevance
  hints.md       # three progressively stronger hints, revealed individually
  examples.md    # independent runnable inputs with verified expected printed output
  starter.py     # public signature and bounded TODOs
  reference.py   # independently authored teaching solution
  solution.md    # reasoning, complexity, alternatives, common mistakes
  cases.py       # public and hidden deterministic contract checks
```

`problem.md` is the learner-facing statement. Avoid a redundant `statement.md` copy: there should be one source of truth for the task. `examples.md` documents expected observable outputs; it does not replace public/hidden test code. Private notes and learner submissions are user data rather than authored Markdown files.

The next foundation lessons live separately while they are **planned**:

```text
content/planned/<robotics-topic>/<stable-slug>/
  metadata.md    # planned status, physical contract, prerequisites, paper applications
  statement.md   # proposed input/output/error contract
  theory.md      # 300–500 words of robotics intuition, defined math, and worked reasoning
  hints.md       # three progressively stronger hints
  examples.md    # two hand-verified inputs and expected outcomes
```

These folders contain no runnable code and do not increase the implemented-problem count. When a lesson is approved for implementation, promote its statement into the single canonical `problem.md`, complete the live folder contract, and run the reference/evaluator quality gates. Do not maintain competing statement copies.

## Theory standard: detailed reasoning within a short lesson

Aim for 350–650 words for a focused component. Depth comes from explaining the assumptions and intermediate steps rather than listing paper history. The present ten lessons are approximately 366–467 words each.

1. Begin with the physical or computational intuition in plain language.
2. Define each symbol, tensor axis, unit, frame, mask, and convention before using it.
3. Show the essential equation in LaTeX and connect its terms to code variables.
4. Work through small numbers to a concrete output; include one invariance or boundary check.
5. Connect the mechanism to the interactive visual and a text/table alternative.
6. Explain why a mistake matters on a robot, then name the likely failure mode.
7. Link the primary source and state the teaching simplification.

The three hints progress from conceptual orientation to an implementation strategy and then a boundary/debugging check. They should not immediately paste the full solution. Expected outputs must be generated from the reviewed reference and checked independently for plausibility; round only displayed values, never the returned result.

## Assessment and editorial gates

- Public examples teach the contract; hidden cases cover other documented valid inputs and boundaries.
- Grade numerical tolerance, shape/dtype/device behavior, immutable inputs, and deterministic ordering where required.
- Preserve gradients for the two PyTorch objectives. Finite output alone does not prove a correct derivative.
- Explain system-task failures through located issues or complete gate reasons, rather than a single unexplained score.
- Keep fixtures synthetic or explicitly licensed and paper summaries independently written.
- Require a reference run, expected-output verification, metadata validation, and rendered Theory review before treating a problem as ready.

## Fifteen planned robotics foundations

Every row links to its statement; adjacent files contain Theory, hints, examples, and planning metadata. None is runnable yet. Paper connections are applications that benefit from the concept, not claims that a reduced exercise reproduces that paper.

| Order | Planned lesson | Prerequisite concepts/problems | Practical result and later paper connection |
|---:|---|---|---|
| F01 | [Compose and invert frame transforms](planned/frames/compose-frame-transforms/statement.md) | Live SE(3) transform | A consistent world/base/camera calibration chain; BEVFormer and SLAM |
| F02 | [Serial-chain forward kinematics](planned/kinematics/serial-chain-forward-kinematics/statement.md) | F01 | Link endpoints and tool pose from a configuration; cuRobo and IK-Geo context |
| F03 | [Planar two-link inverse kinematics](planned/kinematics/planar-two-link-ik/statement.md) | F02 | One declared elbow branch plus reachability status; tool-pose planning |
| F04 | [Geometric Jacobian](planned/kinematics/geometric-jacobian/statement.md) | F01–F02 | Frame-consistent joint-rate to tool-twist map; differential control |
| F05 | [Camera reprojection residuals](planned/calibration/reprojection-residuals/statement.md) | Live camera projection and F01 | Pixel residuals and a defined RMSE; visual SLAM and camera diagnostics |
| F06 | [Joint state at camera time](planned/sensing/interpolate-joint-state/statement.md) | Measurement timestamps and unwrapped joint coordinates | Aligned robot/image observations with explicit gap validity; multimodal episodes |
| F07 | [Differential-drive odometry](planned/estimation/differential-drive-odometry/statement.md) | F01, F06 | A constant-twist world pose update from wheel travel; later sensor fusion |
| F08 | [Kalman position measurement update](planned/estimation/kalman-position-update/statement.md) | F07 and uncertainty interpretation | Posterior position, variance, gain, and innovation; visual-inertial-estimation concepts |
| F09 | [Occupancy log-odds update](planned/mapping/occupancy-log-odds/statement.md) | F01 | A map-cell belief with prior correction; mapping before learned spatial features |
| F10 | [PID with conditional anti-windup](planned/control/pid-anti-windup/statement.md) | F06 | Bounded command and explicit controller memory; executing learned policy targets |
| F11 | [Time-parameterized joint trajectory](planned/control/trajectory-interpolation/statement.md) | F06 | Desired joint position and interval velocity; ACT/action-chunk execution |
| F12 | [Shortest route on a grid](planned/planning/grid-shortest-path/statement.md) | F09 | A reproducible collision-free route with metric cost; baseline for learned planning |
| F13 | [Segment collision with clearance](planned/planning/segment-collision/statement.md) | F12 | Earliest obstacle contact along a whole motion; reusable planner validity checks |
| F14 | [Pre-grasp pose in the tool frame](planned/manipulation/grasp-approach-frame/statement.md) | F01–F02 | Correct approach direction and offset; Dex-Net-style manipulation context |
| F15 | [Episode success and task coverage](planned/evaluation/episode-success-report/statement.md) | Live robot episode contract | Per-task/micro/macro outcomes without hiding missing evidence; robot policy evaluation |

## Recommended concept-to-paper progression

1. **Describe the physical scene:** live SE(3) and projection → F01/F05/F06. Frame names, units, and measurement time become habits before adding model complexity.
2. **Make robot geometry concrete:** F02/F03/F04/F14. Use numerical pose checks and the planned MuJoCo sidecar to explain reachability, branches, axes, and contact approach. Isaac Sim is an optional later backend.
3. **Estimate and represent the world:** F07/F08/F09 → SLAM/BEV paper components. Distinguish a measured state, an uncertain belief, and a map representation.
4. **Propose and execute motion:** F12/F13 plus F10/F11. Check path validity and actuator/time contracts before treating a learned action sequence as executable motion.
5. **Add learned representations and policies:** live IoU/decoder/NMS, CLIP, action codec, and diffusion noising → their reviewed paper tracks. Explain every abstraction through the physical/data contract it consumes.
6. **Evaluate and operate:** live schema validator → F15 → live release gate. Keep task coverage, interventions, collisions, latency, and data lineage visible.

This is a prerequisite graph, not a requirement to finish every branch before attempting a paper mechanism. Each lesson should link to the smallest useful prerequisite and provide a short conceptual recap.

## Coverage limits and next planning decisions

The fifteen plans cover an initial concept spine, not a complete robotics degree. The following gaps should be filled deliberately rather than by creating many near-duplicate exercises:

- **Frames/calibration:** quaternion interpolation, camera distortion, hand-eye calibration, clock-offset estimation, and rolling-shutter assumptions.
- **Kinematics/dynamics:** damped least-squares IK, joint-limit handling, rigid-body dynamics, torque limits, and contact-aware control.
- **Uncertainty/mapping:** prediction covariance, multivariate/EKF updates, data association, loop closure, 3D occupancy, and dynamic obstacles.
- **Planning/control:** smooth/jerk-limited trajectories, RRT-style configuration-space planning, MPC, arm self-collision, and moving obstacles.
- **Manipulation:** grasp width, contact/friction, force control, tactile sensing, and execution-time grasp-quality evaluation.
- **Learning/operations:** behavior-cloning evaluation, receding-horizon policy execution, uncertainty on success rates, dataset leakage, deployment drift, and hardware-in-the-loop evidence.

Before implementing one of these extensions, choose the practical observable result, resolve its prerequisites, and verify the relevant paper's exact mechanism. Research collection growth alone does not promote a paper into runnable curriculum.
