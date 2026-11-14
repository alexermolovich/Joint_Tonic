---
{
  "schema_version": 1,
  "problem_id": "radial-tangential-lens-distortion",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Apply Radial and Tangential Lens Distortion",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.distort_normalized_points",
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
  "physical_contract": {
    "frames": [
      "camera normalized image plane"
    ],
    "units": {
      "points": "dimensionless x=X/Z,y=Y/Z",
      "coefficients": "dimensionless"
    },
    "axes": "Camera x right, y down, z forward; distortion precedes intrinsic pixel projection.",
    "timestamp_assumptions": "One fixed calibration snapshot applies to all points.",
    "batching": "points(N,2), coefficients(5,) -> fresh float64(N,2)."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-input",
      "independent-oracle",
      "immutability"
    ],
    "performance_class": "cpu",
    "evaluator_sha256": "cc968b335cc1f4320c290621313b8dd705c7d2d4ca39555e3badbb889d832f1c"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [
      "https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html"
    ],
    "implementation_urls": []
  },
  "summary": "Apply a five-coefficient radial/tangential lens model to normalized image-plane points.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "camera-calibration"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Apply Radial and Tangential Lens Distortion

Apply a five-coefficient radial/tangential lens model to normalized image-plane points.

```python
def distort_normalized_points(points, coefficients):
```

## Contract

Coefficient order is [k1,k2,p1,p2,k3]. Points must have absolute coordinates <=10; coefficients absolute values <=1. Empty points (0,2) are valid. Apply the Brown-Conrady polynomial written in Theory. No inverse distortion, camera intrinsics, pixel clipping, or fisheye model.

**Shapes and outputs:** points(N,2), coefficients(5,) -> fresh float64(N,2).

**Units:** points: dimensionless x=X/Z,y=Y/Z, coefficients: dimensionless. **Time:** One fixed calibration snapshot applies to all points.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `points=[[1,0],[0,1]], coefficients=[0.1,0,0,0,0]` â†’ `[[1.1,0],[0,1.1]]`.
2. `points=[[1,0]], coefficients=[0,0,0.1,0.2,0]` â†’ `[[1.6,0.1]]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
