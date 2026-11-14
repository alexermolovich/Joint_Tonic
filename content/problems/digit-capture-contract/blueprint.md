---
{
  "schema_version": 1,
  "problem_id": "digit-capture-contract",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Validate a Tactile Image Capture Contract",
  "summary": "A usable tactile frame needs reliable capture metadata as well as pixels.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2020-digit-tactile-sensor",
    "policy-components"
  ],
  "paper_ids": [
    "2020-digit-tactile-sensor"
  ],
  "paper_sections": [
    "Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety."
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
  "entrypoint": "solution.capture_health",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata."
    },
    "axes": "Capture, image row/column/channel, action and candidate axes defined in the contract",
    "timestamp_assumptions": "One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion.",
    "batching": "Capture, image row/column/channel, action and candidate axes defined in the contract"
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
    "authoring_notes": "Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.",
    "primary_urls": [
      "https://arxiv.org/abs/2005.14679"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2020-digit-tactile-sensor.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Validate a Tactile Image Capture Contract

## Contract

`frames` must be a NumPy uint8 array `(N, H, W, 3)`, where `0 <= N <= 64` and `1 <= H, W <= 64`. `timestamps` is real `(N,)` in `[0, 1_000_000]` seconds, `frame_ids` is integer `(N,)` in `[0, 1_000_000]`, and `exposure_us` is real `(N,)` in `[1, 1_000_000]` microseconds. `expected_exposure_us` is a scalar in the same exposure range; `max_gap` is a scalar in `[1e-6, 100]` seconds. Records come from one sensor and clock, in acquisition order; report anomalies without reordering them.

Return a dictionary containing:

- `flags`: Boolean `(N, 4)`, ordered bad time step, discontinuous frame ID, exposure shift, saturation.
- `usable`: Boolean `(N,)`, true where no flag is set.
- `saturation_fraction`: float64 `(N,)`, the fraction of all channel values equal to 0 or 255.
- `ready`: Python bool, true only when at least one frame exists and every frame is usable.

The first row has false time/ID flags. Later rows have a bad time flag when the timestamp difference is nonpositive or exceeds `max_gap`; an ID flag when the identifier increment differs from one. Exposure shifts are flagged when `abs(exposure - expected) > 0.05*expected`. Saturation is flagged when its fraction is strictly greater than 0.95. Equality at the positive gap, exposure and saturation thresholds passes. Empty capture is not ready.

Malformed input formats raise ValueError. These original operational thresholds are quality heuristics, not DIGIT contact detection or force calibration.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
