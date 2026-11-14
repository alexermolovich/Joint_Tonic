---
{
  "schema_version": 1,
  "problem_id": "geometric-jacobian-joint-axes",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute a Geometric Jacobian from Joint Axes",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.geometric_jacobian",
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
      "one right-handed base frame for every input"
    ],
    "units": {
      "origins,tool": "metres",
      "axes": "dimensionless unit vectors",
      "joint_rates": "revolute rad/s; prismatic m/s",
      "twist": "linear m/s then angular rad/s"
    },
    "axes": "Positive rotation follows the right-hand rule; positive prismatic motion follows its axis.",
    "timestamp_assumptions": "All origins and axes describe the same static robot configuration.",
    "batching": "origins/axes(N,3), joint_types list/tuple(N), tool(3,) -> float64 J(6,N); 1<=N<=1000."
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
    "evaluator_sha256": "adf1a5227e47b81f17736faca927376bb627b3c62ebfdd23c2bc087206818250"
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
  "summary": "Convert base-frame joint axes and origins into a linear-first tool geometric Jacobian.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "kinematics"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "serial-chain-forward-kinematics"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Compute a Geometric Jacobian from Joint Axes

Convert base-frame joint axes and origins into a linear-first tool geometric Jacobian.

```python
def geometric_jacobian(origins, axes, joint_types, tool):
```

## Contract

Joint types must be strings "R" or "P". Each axis norm must differ from 1 by at most 1e-7; do not silently renormalize. Top three rows map joint rates to tool-origin linear velocity; bottom three map to angular velocity. Revolute column is concatenate(cross(axis,tool-origin),axis); prismatic column is concatenate(axis,zeros(3)). The types container must be a list or tuple.

**Shapes and outputs:** origins/axes(N,3), joint_types list/tuple(N), tool(3,) -> float64 J(6,N); 1<=N<=1000.

**Units:** origins,tool: metres, axes: dimensionless unit vectors, joint_rates: revolute rad/s; prismatic m/s, twist: linear m/s then angular rad/s. **Time:** All origins and axes describe the same static robot configuration.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `origins=[[0,0,0]], axes=[[0,0,1]], joint_types=["R"], tool=[2,0,0]` â†’ column `[0,2,0,0,0,1]`.
2. Same origin/tool with `axes=[[1,0,0]], joint_types=["P"]` â†’ column `[1,0,0,0,0,0]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
