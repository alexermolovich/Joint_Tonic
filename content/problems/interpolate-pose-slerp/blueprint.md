---
{
  "schema_version": 1,
  "problem_id": "interpolate-pose-slerp",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Interpolate a Pose with SLERP",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.interpolate_pose",
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
      "fixed right-handed world frame"
    ],
    "units": {
      "positions": "metres",
      "quaternions,fraction": "dimensionless"
    },
    "axes": "Quaternions are scalar-first Hamilton (w,x,y,z), active rotations into world coordinates.",
    "timestamp_assumptions": "fraction parametrizes two synchronized endpoint poses; no timestamp extrapolation.",
    "batching": "positions(3,), quaternions(4,), scalar fraction -> (float64 position(3,), quaternion(4,))."
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
    "evaluator_sha256": "335e0eda6d7786d9db5d9bd27b9cc4580b451b150361dc5b2a36f3185044cc90"
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
  "summary": "Interpolate translation linearly and orientation along the shortest quaternion arc.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "geometry"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "normalize-multiply-quaternions"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Interpolate a Pose with SLERP

Interpolate translation linearly and orientation along the shortest quaternion arc.

```python
def interpolate_pose(p0, q0, p1, q1, fraction):
```

## Contract

Both quaternions must be nonzero and are normalized with max-component scaling. Fraction lies in [0,1]. Negate normalized q1 if dot(q0,q1)<0 to choose the shorter arc; exactly zero dot is not negated. For adjusted dot>0.9995 use normalized linear quaternion interpolation; otherwise use SLERP. Normalize the final quaternion. Preserve the q0-aligned sign convention, so the returned endpoint quaternion may equal -normalized(q1).

**Shapes and outputs:** positions(3,), quaternions(4,), scalar fraction -> (float64 position(3,), quaternion(4,)).

**Units:** positions: metres, quaternions,fraction: dimensionless. **Time:** fraction parametrizes two synchronized endpoint poses; no timestamp extrapolation.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `p0=[0,0,0], q0=[1,0,0,0], p1=[2,0,0], q1=[0,0,0,1], fraction=0.5` â†’ position `[1,0,0]`, quaternion `[sqrt(0.5),0,0,sqrt(0.5)]`.
2. Same positions, `q0=[2,0,0,0], q1=[-3,0,0,0], fraction=0.5` â†’ position `[1,0,0]`, quaternion `[1,0,0,0]`; opposite signs describe the same orientation.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Quaternion coordinate order is scalar-first (w,x,y,z); both orientations and positions use the same right-handed reference frame.
