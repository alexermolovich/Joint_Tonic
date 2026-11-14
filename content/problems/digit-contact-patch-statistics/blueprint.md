---
{
  "schema_version": 1,
  "problem_id": "digit-contact-patch-statistics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Estimate Contact Patch Statistics",
  "summary": "A contact candidate mask can be summarized by its area, center and spread in the image.",
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
  "entrypoint": "solution.contact_patch_statistics",
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

# Estimate Contact Patch Statistics

## Contract

`mask` is Boolean `(B, H, W)`, with `1 <= B <= 128` and `1 <= H, W <= 64`. Return a dictionary containing:

- `area`: int64 `(B,)`, number of selected pixels.
- `centroid`: float64 `(B, 2)` in `(x=column, y=row)` order.
- `covariance`: float64 `(B, 2, 2)`, the population mean of centered coordinate outer products over selected pixels.
- `bounds`: int64 `(B, 4)` in `(xmin, ymin, xmax_exclusive, ymax_exclusive)` order.

Integer coordinates denote pixel centers. A single pixel has zero covariance. An empty region has area 0, NaN centroid and covariance, and all bounds equal to -1. Aggregate all selected pixels; do not split connected components. Area is a pixel count, centroid uses pixels and covariance uses squared pixels. No physical surface-area or force conversion is implied.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
