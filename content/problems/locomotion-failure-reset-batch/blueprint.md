---
{
  "schema_version": 1,
  "problem_id": "locomotion-failure-reset-batch",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Reset Failed Locomotion Environments",
  "summary": "Reset logic should identify why an episode ended before replacing state.",
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
  "entrypoint": "solution.reset_failed_locomotion",
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

# Reset Failed Locomotion Environments

## Contract

Contact force real(B,K,3) Newtons,0<=B<=4096,0<=K<=16 (caller-selected termination contact bodies),abs<=1e4. Episode steps integer(B,)0..1e6; max_steps built-in int1..1e6. State/initial real(B,D),1<=D<=64, abs<=1e4, caller-declared matched units and frame. last_action real(B,A),1<=A<=32 normalized[-1,1]; feet_air_time real(B,F),1<=F<=8 seconds[0,100]. Failure any selected body Euclidean force norm>1 N; timeout episode_steps>max_steps (strict released convention). Reset=failure OR timeout. Return dict failure,timeout,reset bool(B,), state float64(B,D) from initial where reset else state, last_action and feet_air_time with reset rows zeroed, episode_steps int64(B) reset to0. Empty K produces no contact failures. Both failure and timeout can be true; preserve both. Reset states supplied deterministically, no command randomization, controller actuation or episode-version increment. Generic selective reset exercise remains prerequisite; this adds locomotion termination signals and action/contact history clearing.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
