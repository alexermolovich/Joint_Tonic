---
{
  "schema_version": 1,
  "problem_id": "hilserl-intervention-segments",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Label Human Intervention Segments",
  "summary": "A human override changes the action that the robot actually experiences.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-hil-serl",
    "policy-components"
  ],
  "paper_ids": [
    "2024-hil-serl"
  ],
  "paper_sections": [
    "Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety."
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
  "entrypoint": "solution.label_interventions",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers."
    },
    "axes": "Record, trial, controller-channel and source dimensions are declared in the contract",
    "timestamp_assumptions": "Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence.",
    "batching": "Record, trial, controller-channel and source dimensions are declared in the contract"
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
    "authoring_notes": "Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.",
    "primary_urls": [
      "https://arxiv.org/abs/2410.21845"
    ],
    "paper_card": "research/papers/robot-learning-rl/2024-hil-serl.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Label Human Intervention Segments

## Contract

policy_actions/human_actions real(N, A), intervention bool(N,), episode_ids int(N,)nonnegative nondecreasing<=1e6; 0<=N<=16384,1<=A<=16, actions normalized[-1,1]. Both proposed and human commands validated even when not selected. Return dict executed_actions float64(N, A) chosen human when intervention else policy; segment_id int64(N,) -1 on autonomous rows, consecutive 0-based ID for each maximal contiguous human run inside one episode; segments int64(K,3) rows[episode ID, start index, end index exclusive] ordered by start. Consecutive human rows across episode boundary are separate segments. Recorded action sources do not set terminal flags; this task does not infer task completion. All commands share the caller-declared controller frame/control interval; no position-to-velocity conversion.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
