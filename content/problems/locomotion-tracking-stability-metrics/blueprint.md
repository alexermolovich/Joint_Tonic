---
{
  "schema_version": 1,
  "problem_id": "locomotion-tracking-stability-metrics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute Gait Tracking and Stability Metrics",
  "summary": "Command tracking and body stability describe different parts of locomotion.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2021-learning-to-walk-in-minutes",
    "policy-components"
  ],
  "paper_ids": [
    "2021-learning-to-walk-in-minutes"
  ],
  "paper_sections": [
    "Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic."
  ],
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
  "entrypoint": "solution.gait_metrics",
  "physical_contract": {
    "frames": [
      "Right-handed robot base x forward/y left/z up; terrain positions/origins in one world frame"
    ],
    "units": {
      "values": "Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract."
    },
    "axes": "Environment, time, body-contact and controller-channel axes are defined in the contract",
    "timestamp_assumptions": "Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed.",
    "batching": "Environment, time, body-contact and controller-channel axes are defined in the contract"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.",
    "primary_urls": [
      "https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2021-learning-to-walk-in-minutes.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute Gait Tracking and Stability Metrics

## Contract

Arrays velocity/angular/command/gravity real(B,T,3),0<=B<=128,1<=T<=256, abs<=100 except gravity unit vectors with norm1 atol1e-7. Commands columns desired base-frame vx,vy (m/s), yaw rate wz (rad/s); linear/angular measurements in same right-handed base frame with x forward,y left,z up. Projected gravity is the world unit downward vector expressed in body coordinates. Valid bool(B,T); scales positive [1e-6,1000] with linear_scale (m/s)^2 and yaw_scale (rad/s)^2. Per valid sample tracking errors ev=(vx-cx)^2+(vy-cy)^2 and ew=(wz-cw)^2; rewards exp(-ev/linear_scale),exp(-ew/yaw_scale). Stability diagnostics: vertical velocity squared vz^2 in(m/s)^2, roll/pitch angular rate squared wx^2+wy^2 in(rad/s)^2, tilt penalty gx^2+gy^2 dimensionless. Return dict per_step float64(B,T,5) ordered [linear_reward,yaw_reward,vertical_penalty,angular_penalty,tilt_penalty] with invalid zero; counts int64(B), means float64(B,5), NaN rows with no valid samples. No sum of unlike-unit penalties or configured reward weights/time-step factors. These scalar terms match released reward mechanisms; reporting masks/means are original diagnostics.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
