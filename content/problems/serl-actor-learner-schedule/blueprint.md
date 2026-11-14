---
{
  "schema_version": 1,
  "problem_id": "serl-actor-learner-schedule",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Schedule Actor-Learner Updates",
  "summary": "The learner should not consume an unbounded update budget merely because it runs faster than robot collection.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-serl",
    "policy-components"
  ],
  "paper_ids": [
    "2024-serl"
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
  "entrypoint": "solution.schedule_learner",
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
      "https://arxiv.org/abs/2401.16013"
    ],
    "paper_card": "research/papers/robot-learning-rl/2024-serl.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Schedule Actor-Learner Updates

## Contract

new_transitions integer(T,) in[0,10000],0<=T<=4096; warmup built-in int[0,1e6], ratio_numerator/denominator built-in ints1..32, max_updates_per_tick int 1..1000, publish_every int 1..1000. All counters start at 0. At tick t cumulative data D=sum of new transitions; target updates=floor(max(D-warmup,0)*numerator/denominator) using exact integer arithmetic. Emit min(max_updates_per_tick, target updates-completed updates); backlog carries across ticks including ticks with no new data. Each optimizer update increments model version by1. Publish the latest completed version when floor(completed/publish_every) increases since previous tick, else keep prior published version. Return dict updates int64(T,), completed int64(T,), backlog int64(T,), published_version int64(T,), publish bool(T,). A crossing can skip versions; publish current latest once rather than inventing many network messages. Original synchronous accounting model of an asynchronous actor/learner schedule; no wall-clock or hardware throughput guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
