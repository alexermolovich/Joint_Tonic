---
{
  "schema_version": 1,
  "problem_id": "exponential-trajectory-weights",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Normalize Exponential Trajectory Cost Weights",
  "summary": "Convert supplied corrected rollout costs into stable normalized weights.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "path-integral-mpc"
  ],
  "paper_ids": [
    "2015-path-integral-mpc"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2015-path-integral-mpc"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.trajectory_weights",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "deb84965a3900f9a8dc826a4030d7c3596c600bc780a57202231e8b9e59a4062"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1509.01149"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Normalize Exponential Trajectory Cost Weights

Implement `trajectory_weights(costs, valid, temperature)`.

Convert supplied corrected rollout costs into stable normalized weights.

`costs` float64 `(N,)`, `valid` bool `(N,)`, `1<=N<=16384`, with at least one valid entry. Costs use one common caller-defined cost unit. `temperature` is Python int/float in `[1e-6,1e6]` in the same units. For valid entries use `exp(-(cost-min_valid_cost)/temperature)` and normalize over valid entries; invalid weights are exactly zero. Return dict `weights`: fresh float64 `(N,)`, `effective_samples`: Python float `1/sum(weights²)`, and `best_index`: Python int, lowest original index attaining the minimum valid cost. Invalid entries must still satisfy numeric validation. These are supplied corrected MPPI rollout costs, including any required control/importance terms; the exercise does not derive those terms or run a dynamics model. There is no spatial frame or time integration in this reduction.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Costs `[0.,log(3)]`, both valid, temperature1 gives weights `[0.75,0.25]`, effective samples `1.6`, best index0.
2. Costs `[2.,-100.,2.]`, validity `[True,False,True]`, temperature1 gives weights `[0.5,0.,0.5]`, effective samples2, best index0.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(N) time and memory. Mask before finding the stabilizing minimum; an invalid low-cost rollout must not affect normalization or best-index selection.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
