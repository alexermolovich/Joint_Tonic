---
{
  "schema_version": 1,
  "problem_id": "serl-intervention-reset-statistics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Record Intervention and Reset Statistics",
  "summary": "Training time, human effort and reset overhead describe different costs.",
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
  "entrypoint": "solution.interaction_statistics",
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

# Record Intervention and Reset Statistics

## Contract

three durations real(N,)seconds[0,1e6], intervention_duration<=trial_duration; task_success/reset_success/valid bool(N,),0<=N<=16384. trial_duration excludes reset; intervention_duration is human-control time within trial. Return dict trials Python int valid count, autonomous_trials Python int count valid with intervention_duration==0; robot_time Python float sum(trial+reset)valid; human_time Python float sum intervention valid; reset_time Python float sum reset valid; human_fraction Python float human_time/sum trial or NaN when zero; task_success_rate/reset_success_rate Python float valid mean or NaN; autonomous_success_rate Python float success mean over valid zero-intervention trials or NaN. All masked durations still validated. Zero-duration autonomous trials permitted but their time fraction remains undefined if total trial time 0. Human assistance and resets are separate accounting categories; totals do not certify comparable initial-state distributions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
