---
{
  "schema_version": 1,
  "problem_id": "validate-camera-calibration-matrix",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Validate a Camera Calibration Matrix",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.validate_camera_matrix",
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
      "camera image pixel plane"
    ],
    "units": {
      "K": "focal lengths,skew,principal point in pixels; homogeneous bottom row dimensionless",
      "width,height": "pixels"
    },
    "axes": "u right, v down; principal point must lie inside the declared image.",
    "timestamp_assumptions": "Matrix and image dimensions refer to the same calibrated image stream.",
    "batching": "K(3,3), integer width,height -> Python bool."
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
    "evaluator_sha256": "d499ce19ec497b6c6d33c53d0fe82013e52b78c93b1f9680b3fb5e97bfdc51ca"
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
  "summary": "Check a pinhole intrinsic matrix against an explicit image-size and principal-point policy.",
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

# Validate a Camera Calibration Matrix

Check a pinhole intrinsic matrix against an explicit image-size and principal-point policy.

```python
def validate_camera_matrix(K, width, height):
```

## Contract

width,height must be built-in or NumPy integers in [1,100000], not bool. K must be finite real (3,3); malformed shapes/types raise ValueError. For well-formed K return True exactly when fx=K[0,0]>0, fy=K[1,1]>0, 0<=cx=K[0,2]<width, 0<=cy=K[1,2]<height, and K[1,0],K[2,0],K[2,1] are within 1e-9 of zero and K[2,2] within 1e-9 of one. Skew K[0,1] is unrestricted within numeric bounds. A well-formed matrix that violates these calibration conditions returns False, not an exception.

**Shapes and outputs:** K(3,3), integer width,height -> Python bool.

**Units:** K: focal lengths,skew,principal point in pixels; homogeneous bottom row dimensionless, width,height: pixels. **Time:** Matrix and image dimensions refer to the same calibrated image stream.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `K=[[500,0,320],[0,510,240],[0,0,1]], width=640, height=480` â†’ `True`.
2. Same K with width=320 â†’ `False` because cx equals the excluded right boundary.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
