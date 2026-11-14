---
{
  "schema_version": 1,
  "problem_id": "hand-eye-translation-residual",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Solve a Small Hand-Eye Calibration Residual",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.solve_hand_eye_translation",
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
      "gripper relative motion A",
      "camera relative motion B",
      "fixed camera-to-gripper X"
    ],
    "units": {
      "translations,residuals": "metres",
      "rotations": "dimensionless"
    },
    "axes": "Right-handed active homogeneous transforms; AX=XB order is part of the contract.",
    "timestamp_assumptions": "A[i],B[i] are corresponding relative motions from synchronized pose pairs.",
    "batching": "A/B(N,4,4), rotation(3,3), 2<=N<=1000 -> translation float64(3,), residuals float64(N,3)."
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
    "evaluator_sha256": "47453c2b2fec7ab2e2915d151ddcd0e206fc39451cf2ebff4cb7734a0a657a91"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [],
    "implementation_urls": []
  },
  "summary": "Solve the translation component of AX=XB with a supplied hand-eye rotation and report per-pair residuals.",
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

# Solve a Small Hand-Eye Calibration Residual

Solve the translation component of AX=XB with a supplied hand-eye rotation and report per-pair residuals.

```python
def solve_hand_eye_translation(A, B, rotation):
```

## Contract

All transforms must be proper rigid matrices: bottom row [0,0,0,1], rotation orthogonality and determinant +1 within atol=1e-8. Rotation is the fixed, already estimated R_X; this problem does not estimate it. Stack C_i=R_Ai-I and d_i=R_X t_Bi-t_Ai. Solve min_t ||Ct-d||Â² using np.linalg.lstsq rcond=1e-10. Raise ValueError if its reported rank<3. Return t and (Ct-d).reshape(N,3), including nonzero residuals for noisy/inconsistent data. Do not enforce the rotational AX=XB equation; only the translation residual is solved.

**Shapes and outputs:** A/B(N,4,4), rotation(3,3), 2<=N<=1000 -> translation float64(3,), residuals float64(N,3).

**Units:** translations,residuals: metres, rotations: dimensionless. **Time:** A[i],B[i] are corresponding relative motions from synchronized pose pairs.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. Let both A translations be zero, R_A1=diag(1,-1,-1), R_A2=diag(-1,1,-1), and R_X=I. Use B with the same respective rotations and translations `[0,-4,-6]`, `[-2,0,-6]`. Return t=`[1,2,3]` and zero residuals.
2. Same rotations with every A/B translation zero returns t=`[0,0,0]` and zero residuals. Repeating only the first rotation instead must raise ValueError.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
