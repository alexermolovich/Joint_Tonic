---
{
  "schema_version": 1,
  "problem_id": "hilserl-mix-corrective-replay",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Mix Intervention and Autonomous Replay",
  "summary": "Corrective and autonomous transitions answer different questions.",
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
  "entrypoint": "solution.mix_corrective_replay",
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

# Mix Intervention and Autonomous Replay

## Contract

executed_actions real(N, A)normalized[-1,1], intervention bool(N,), priorities real(N,)in[0,1),0<=N<=16384,1<=A<=16; batch_size built-in int 0..4096; intervention_fraction scalar[0,1]. Human quota=floor(batch_size*fraction+.5) (half up), autonomous quota=batch-human. Require enough distinct records in each pool; no silent quota adjustment. Within each pool choose quota lowest supplied priorities, tie lowest original index, without replacement. Output selected human rows first then autonomous rows, each in priority/index order. Return dict indices int64(B,), actions float64(B, A), intervention bool(B,), counts int64(2,)ordered[human, autonomous]. Priorities may be recorded random draws but no RNG inside function. Supplied actions are executed actions, not overwritten policy proposals. This original source-exclusive sampling recipe is not claimed to exactly match HIL-SERL's potentially overlapping online/demonstration buffer layout.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
