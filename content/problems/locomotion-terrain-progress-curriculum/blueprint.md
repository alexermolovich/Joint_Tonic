---
{
  "schema_version": 1,
  "problem_id": "locomotion-terrain-progress-curriculum",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Sample Terrain Difficulty by Policy Progress",
  "summary": "A terrain curriculum changes difficulty from measured progress rather than a generic success label.",
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
  "entrypoint": "solution.update_terrain_levels",
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

# Sample Terrain Difficulty by Policy Progress

## Contract

Levels integer(B,),0<=B<=16384,0<=level<num_levels; positions/origins real(B,2) world-frame horizontal meters abs<=1e4; commands real(B,2) horizontal robot-base-frame m/s abs<=100 (its speed norm is invariant to a horizontal yaw rotation); reset bool(B,); restart_draws real(B,) in[0,1). terrain_length scalar[1e-3,1e4] meters; episode_seconds scalar[1e-3,1000]seconds; num_levels built-in int1..1024. For resetting environments only, distance=norm(position-origin). move_up=distance>terrain_length/2; move_down=(distance<norm(command)*episode_seconds/2) AND NOT move_up. Candidate level=level+up-down. If >=num_levels, replace with floor(draw*num_levels); else clip at minimum0. Other levels unchanged. Return dict levels int64(B,), move_up/move_down/reassigned bool(B,), distance float64(B,) for all environments. Supplied draws replace official random reassignment to make replay deterministic; this is subsequent-reset curriculum only (initial reset is caller responsibility). Does not generate terrain geometry or update origin lookup; no direction-of-travel success claim. Promotion takes precedence if both raw criteria would hold.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
