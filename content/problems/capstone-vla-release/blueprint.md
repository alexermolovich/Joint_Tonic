---
{
  "schema_version": 1,
  "problem_id": "capstone-vla-release",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Build and Evaluate a Bounded VLA Release",
  "summary": "Train a bounded policy adapter, generate action tokens, and evaluate held-out robot episodes before a synthetic release.",
  "type": "integration",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "physical-ai"
  ],
  "topics": [
    "capstone",
    "vla-release"
  ],
  "paper_ids": [
    "2024-openvla",
    "2022-rt-1"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2024-openvla"
  ],
  "prerequisite_problem_ids": [
    "build-robot-sequence-validity-masks",
    "openvla-lora-policy-layer",
    "rt1-action-codec"
  ],
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
  "entrypoint": "solution.vla_release",
  "physical_contract": {
    "frames": [
      "Declared optical camera/world frames or explicitly nonspatial feature axes"
    ],
    "units": {
      "values": "Meters, pixels, milliseconds, normalized features and rates as defined in the contract"
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
      "Two end-to-end worked examples"
    ],
    "hidden_case_families": [
      "Independent scalar mechanism oracle",
      "Failure path and missing evidence",
      "Invalid inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "efd99d329904545d7964d5746d6ccd99a2b4b07dba0edc753dbe06155c5236c3"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original cross-paper synthetic integration. Its stage contracts, limits, diagnostics and release policies are teaching choices, not a reproduced trained model or permission to deploy hardware.",
    "primary_urls": [
      "https://arxiv.org/abs/2406.09246",
      "https://arxiv.org/abs/2212.06817"
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

# Build and Evaluate a Bounded VLA Release

Implement `vla_release(observations, targets, valid, train, embodiment, tasks, lower, upper, base, projection, adapter, learning_rate, latency, max_mse, budget_ms)`.

Train a bounded policy adapter, generate action tokens, and evaluate held-out robot episodes before a synthetic release.

`observations` float64 `(B,T,D)` are frozen, dimensionless sensor/language features; `targets` float64 `(B,T,A)` are joint-position targets in radians; `valid` and `train` bool `(B,T)` mark usable and training slots. Require `1<=B,T<=32`, `1<=D,A<=16`. Each row is one robot episode; steps are already ordered at one fixed but caller-declared control period and never cross episode boundaries. `train` must imply valid; at least one training and one held-out valid slot are required. `embodiment` int64 `(B,)` indexes `E` robots (`1<=E<=8`); `tasks` int64 `(B,)` indexes exactly three task labels 0,1,2. `lower,upper` float64 `(E,A)` have gaps at least `1e-6`, values within `[-100,100]`. Valid targets must be inside their embodiment's bounds; invalid targets are ignored after finite/dtype validation.

`base` float64 `(D,A)` and `projection` float64 `(D,R)` are frozen, `adapter` float64 `(R,A)` is trainable, with `1<=R<=D`. Features and all three matrices must have absolute values <=10. `learning_rate` is a Python int/float in `[0,1]`. Normalize valid training targets to `y=2*(target-lower)/(upper-lower)-1`. Fit exactly one gradient step of mean squared normalized error, averaged over training slots and action channels: predictions `x@base+(x@projection)@adapter`; gradient `2/(n_train*A) * (X@projection).T @ (prediction-y)`. Update only adapter.

Predict with the updated adapter at every valid slot. Clip raw normalized actions to `[-1,1]`, encode into 16 uniform bins by `min(15,floor(8*(clipped+1)))`, decode each bin center `-1+(token+0.5)/8`, and map back into per-embodiment radians. Invalid slots get token -1 and action zero. Evaluation uses only held-out slots: `invalid_rate` is the fraction with any raw normalized channel outside `[-1,1]`; `embodiment_mse` `(E,)` and `task_mse` `(3,)` average squared action error across their held-out slots and channels, preserving absent slices as NaN.

`latency` float64 `(B,T)` is supplied duration in milliseconds `[0,10000]`. Compute nearest-rank p95 over held-out slots only. `max_mse` is Python int/float `[0,40000]` in radians squared and `budget_ms` is `[0,10000]`. Return fresh arrays `adapter`, `tokens` int64 `(B,T,A)`, `actions` float64 `(B,T,A)`, `embodiment_mse`, `task_mse`; Python floats `invalid_rate`, `p95_ms`; and `decision='promote'` iff invalid rate is zero, **every represented held-out** task and embodiment MSE is <=max_mse, and p95<=budget_ms, otherwise `hold`. A label seen only in training has no represented held-out slice and its metric remains NaN. `adapter_sha256` is the lowercase SHA256 hex digest of the updated adapter's C-order little-endian float64 bytes. This fingerprints the adapter only, not the complete release; the reproducibility report must also record bounds/base/projection/data versions. No inputs are changed. Time O(BTDRA), with bounded dimensions.

This is an original linear frozen-feature adapter and action-codec integration. It implements neither OpenVLA's transformer nor an autoregressive token model. Held-out slots are explicit; callers must additionally enforce real-world episode/data separation.


## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

### Example 1: fit then evaluate

Use observations `[[[1.],[1.]]]`, targets `[[[0.5],[0.5]]]`, validity `[[True,True]]`, training mask `[[True,False]]`, embodiment/task `[0]`, bounds `[[-1.]]` to `[[1.]]`, base `[[0.]]`, projection `[[1.]]`, adapter `[[0.]]`, learning rate `0.5`, latency `[[100.,5.]]`, max MSE `0.01`, and budget `10`. The updated adapter is `[[0.5]]`; tokens are `[[[12],[12]]]`, actions `[[[0.5625],[0.5625]]]` radians, represented slice MSE is `0.00390625`, other task slices are NaN, held-out p95 is 5 ms, and decision is `promote`. The slow training-slot duration is excluded.

### Example 2: held-out latency failure

Change held-out latency to 20 ms. The adapter, action tokens, and errors stay identical, but p95 becomes 20 ms and decision becomes `hold`. Training success cannot override serving evidence.

## Source and scope

[Primary source](https://arxiv.org/abs/2406.09246). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Follow the stage equations in Theory. The reference composes bounded NumPy operations and explicit validation; it never executes a trained model or contacts a robot. Runtime is linear in supplied tensor entries except the documented buffer allocation search.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
