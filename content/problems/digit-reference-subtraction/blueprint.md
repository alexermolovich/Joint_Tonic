---
{
  "schema_version": 1,
  "problem_id": "digit-reference-subtraction",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Subtract a Tactile Reference Image",
  "summary": "Subtract a comparable unloaded reference to reveal optical change.",
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
  "entrypoint": "solution.tactile_difference",
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

# Subtract a Tactile Reference Image

## Contract

`images` is real `(B, H, W, C)`, `reference` is real `(H, W, C)` and `roi` is Boolean `(H, W)`. Bounds are `1 <= B <= 32`, `1 <= H, W <= 64`, `1 <= C <= 3`, and all intensities lie in `[0, 1]`. `threshold` is a scalar in `[0, 1]`. Captures and unloaded reference must share sensor, pixel alignment and exposure.

Return `difference` (float64 `(B, H, W, C)`) as signed capture-minus-reference, `change` (float64 `(B, H, W)`) as the mean absolute channel difference, and `mask` (Boolean `(B, H, W)`) where change is strictly greater than the threshold, in a dictionary. All three outputs are zero or false outside the ROI. An empty ROI returns all-zero outputs. Broadcast the reference only over the batch axis.

Image rows increase down and columns right; integer coordinates denote pixel centers. Appearance change is neither a force measurement nor proof of contact.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
