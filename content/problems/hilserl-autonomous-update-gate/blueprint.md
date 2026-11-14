---
{
  "schema_version": 1,
  "problem_id": "hilserl-autonomous-update-gate",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Gate an Online Policy Update",
  "summary": "A candidate that succeeds only with human corrections has not shown autonomous improvement.",
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
  "entrypoint": "solution.gate_policy_update",
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

# Gate an Online Policy Update

## Contract

success, safety_violation, assisted, valid bool(2, N),0<=N<=4096; row 0 current, row 1 candidate on a declared fixed evaluation protocol, no paired-seed assumption. current_version/candidate_version built-in int 0..1e9, min_autonomous_trials int 1..4096, allowed_success_drop/max_violation_rate scalar[0,1]. Eligible evidence=valid AND NOT assisted. Compute each row count, success rate, violation rate (NaN absent). Return dict counts int64(2,), success_rate/violation_rate float64(2,), checks bool(4,)ordered[newer_version, both_have_min_trials, candidate_success>=current_success-allowed_drop, candidate_violation<=limit], accepted Python bool all checks. Missing rates make comparisons False. Successful assisted trials cannot improve autonomous evidence. Observed-rate gate only; no uncertainty guarantee, hardware execution authorization or automatic deployment.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
