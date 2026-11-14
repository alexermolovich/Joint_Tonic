---
{
  "schema_version": 1,
  "problem_id": "fr3-joint-interpolation",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Interpolate Franka FR3 Joint Waypoints",
  "summary": "Create evenly spaced joint waypoints and inspect their forward kinematics on a Franka Research 3 in MuJoCo.",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 20,
  "domains": [
    "geometry"
  ],
  "topics": [
    "kinematics",
    "joint-space",
    "simulation"
  ],
  "paper_ids": [],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.interpolate_fr3_joints",
  "physical_contract": {
    "frames": [
      "fr3_joint1..fr3_joint7 local joint coordinates",
      "MuJoCo world/base for displayed attachment pose"
    ],
    "units": {
      "q_start": "radians",
      "q_goal": "radians",
      "output": "radians",
      "displayed_position": "meters"
    },
    "axes": "Positive hinge rotation about each model joint local +z, right-hand rule; MuJoCo world is z-up. Output columns are joints, not Cartesian axes.",
    "timestamp_assumptions": "Uniform dimensionless path samples; no execution duration or velocity guarantee. UI replay speed is display-only.",
    "batching": "Two unbatched vectors (7,), output (num_steps,7); num_steps includes both endpoints."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "three-waypoint-example",
      "stationary-arm",
      "two-endpoints"
    ],
    "hidden_case_families": [
      "model-limit-boundaries",
      "all-seven-joints",
      "invalid-shape-dtype-finite-range",
      "sample-count",
      "input-preservation",
      "maximum-waypoints"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original foundation exercise and synthetic fixtures; official FR3 model is a separate Apache-2.0 asset with retained upstream notices. Kinematic replay, not collision-free planning or physical control.",
    "primary_urls": [
      "https://github.com/google-deepmind/mujoco_menagerie/tree/98a70c569c4c1b6da467a20012f766ee1f8dc521/franka_fr3",
      "https://frankarobotics.github.io/docs/robot_specifications.html",
      "https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-forward"
    ],
    "implementation_urls": []
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": ["root", "fr3_simulator"]
}
---

# Interpolate Franka FR3 Joint Waypoints

## Learning objective

Construct a seven-joint configuration path with explicit endpoints, ordering and joint limits, then relate it to the curved Cartesian path shown by forward kinematics.

## Contract

Implement `interpolate_fr3_joints(q_start, q_goal, num_steps) -> np.ndarray`.

Inputs are real integer/floating array-like vectors of shape `(7,)`. Convert to float64 after rejecting boolean, complex, string and object dtypes. Values must be finite and inside the inclusive model ranges below. Dtype validation applies after `np.asarray`; mixed Python sequences are judged by their resulting NumPy dtype. `num_steps` is a Python/NumPy integer scalar, excluding booleans, from 2 through 101 inclusive. Reject every documented invalid argument with `ValueError` (including conversion/shape failures). Empty vectors and batched inputs are invalid.

| Column | Model joint | Inclusive range (rad) |
|---|---|---|
| 0 | fr3_joint1 | [-2.9007, 2.9007] |
| 1 | fr3_joint2 | [-1.8361, 1.8361] |
| 2 | fr3_joint3 | [-2.9007, 2.9007] |
| 3 | fr3_joint4 | [-3.0770, -0.1169] |
| 4 | fr3_joint5 | [-2.8763, 2.8763] |
| 5 | fr3_joint6 | [0.4398, 4.6216] |
| 6 | fr3_joint7 | [-3.0508, 3.0508] |

Return a new float64 array `(num_steps,7)` without input mutation or memory sharing. Row `k` is `(1-k/(num_steps-1))*q_start + (k/(num_steps-1))*q_goal`, for `k=0,...,num_steps-1`. Preserve the endpoints; do not wrap angles or choose a shorter angular branch. Linear interpolation is a convex combination of model-valid joint positions. Time and memory are O(7*num_steps).

## Physical and visualization scope

The seven coordinates use each FR3 hinge's local +z right-hand rotation, in radians. There is no timestamp input or physical duration. Replay speed is only visual. The trusted simulator applies each row as qpos then calls MuJoCo forward kinematics; it reports `attachment_site` in the fixed world/base frame (+z up), meters and rotation matrix. The model is the actual FR3 arm without a gripper. Joint limits do not establish collision clearance, feasible torque, or safe real-robot motion. No inverse kinematics or dynamics reproduction is claimed.

Public preview fixture: `q_start=[0,0,0,-1.57079,0,1.57079,-0.7853]`, `q_goal=[0.4,-0.3,0.2,-1.8,0.1,1.9,-0.4]`, `num_steps=41`. The preview invokes learner code only inside the existing isolated worker. A bounded validated trajectory is handed to the separate simulator; invalid output produces a preview error, never an author reference fallback.

## Worked examples

1. Start `[0,0,0,-1,0,1,0]`, goal `[0.4,0.2,-0.2,-1.4,0.6,1.4,-0.4]`, 3 rows: start; `[0.2,0.1,-0.1,-1.2,0.3,1.2,-0.2]`; goal.
2. Start equals goal `[0,0,0,-1,0,1,0]`, 4 rows: repeat that vector four times.

## Implementation and grading plan

A small vectorized reference validates dtypes, scalar sample count, shapes, finite values and seven model-specific ranges. NumPy broadcasting constructs the output. Public cases match the examples and the two-endpoint case. Hidden cases exercise reversed direction, mixed joint changes, stationary path, boundary ranges, dtype and invalid inputs, maximum101 samples, deterministic random endpoints and no mutation/aliasing. Numerical tolerance is rtol1e-7/atol1e-9. A starter negative control must fail. Public Run and hidden Submit use the existing isolated CPU worker; MuJoCo display availability must not alter numerical grading.

## Theory and accessibility plan

Original intuition, seven-column shape trace, interpolation math and convex-limit argument, numeric midpoint, distinction between joint-space straightness and Cartesian curvature, robot failure modes, and model provenance. A numerical joint/pose table supplements the rendered scene; manual stepping works without animation. Reduced-motion suppresses automatic playback.

## Provenance and reproducibility

Foundation task, no paper claim. Original synthetic test fixtures are CC0-1.0. Official Menagerie FR3 assets pinned to commit `98a70c569c4c1b6da467a20012f766ee1f8dc521`; retain full Apache-2.0 LICENSE including appended BSD notice. Asset file hashes and simulator runtime/settings live in the simulator lock manifest. Learner runtime Python3.12.3/NumPy2.2.4 matches the local worker; OCI digest remains pending. A future physical-control exercise must add time parameterization, rate/acceleration limits, collision checking and controller-specific safety validation.
