---
{
  "schema_version": 1,
  "problem_id": "bev-bilinear-camera-sampling",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Sample Calibrated Multi-Camera Feature Maps",
  "type": "function",
  "difficulty": "medium",
  "paper_ids": [
    "2022-bevformer"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2022-bevformer"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.sample_camera_features",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator"
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
  "physical_contract": {
    "frames": [
      "Per-camera feature grid: u right, v down"
    ],
    "units": {
      "coordinates": "feature-map pixel-center indices",
      "features": "dimensionless"
    },
    "axes": "C cameras,H rows,W columns,D channels; C,N,2 queries",
    "timestamp_assumptions": "Fixed supplied batch; cameras/observations are aligned by caller. No clock inference, state history or real-time guarantee.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-mechanism-oracle",
      "boundary-and-invalid-input",
      "maximum-advertised-dimensions",
      "input-preservation-and-output-aliasing"
    ],
    "performance_class": "none",
    "evaluator_sha256": "051c4aa70031116cccbe7d6a9dc97fe0f8518941dbed9e40c2bdeb6b50e90277"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2203.17270"
    ],
    "implementation_urls": []
  }
}
---

# Sample Calibrated Multi-Camera Feature Maps

A projected location usually lies between feature-map cells. Bilinear sampling blends nearby cells while preserving a camera-specific validity decision. Projection and calibration are supplied by the caller; this function only gathers aligned visual evidence.

```python
def sample_camera_features(features, coordinates, valid):
    ...
```

## Function contract

Inputs: `features: float64(C, H, W, D)`, `coordinates: float64(C, N, 2)` and `valid: bool(C, N)`. Bounds: `1<=C<=8`, `1<=H, W<=64`, `1<=D<=32`, `0<=N<=4096`. The maximum feature tensor has 1, 048, 576 entries and is supported.

Coordinates `(u, v)` are already projected feature-map pixel-center indices. The caller has applied camera calibration and image-to-feature scaling. Use a query only when its mask is true and it lies in the closed range `0<=u<=W-1`, `0<=v<=H-1`. Bilinearly interpolate four neighbors using floor indices and upper neighbors clipped to the final row/column. Out-of-view or masked queries return exact zero.

Return `samples: float64(C, N, D)` and `used: bool(C, N)`. Validate every coordinate, including unused ones. Cameras are synchronized; no cross-camera attention normalization or physical-frame transform occurs here.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One camera has a single-channel map `[[0, 2],[4, 6]]`. A valid point `(u=.5, v=.5)` samples value `3`, with `used=True`.

**Example 2.** For the same map, points `(1, 1)` and `(1.1, 1)` produce samples `6` and `0`. The returned used mask is `[True, False]`; the second point is outside.

## Source and scope

Original bounded component based on [2022-bevformer](https://arxiv.org/abs/2203.17270). BEV perception combines evidence from calibrated cameras. Using original image coordinates directly on a downsampled feature map selects the wrong evidence. An out-of-view point must not be clipped into a plausible border observation.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
