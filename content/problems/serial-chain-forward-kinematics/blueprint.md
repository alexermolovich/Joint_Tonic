---
{
  "schema_version": 1,
  "problem_id": "serial-chain-forward-kinematics",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute Forward Kinematics for a Serial Chain",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.planar_forward_kinematics",
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
      "fixed base xy plane",
      "tool frame"
    ],
    "units": {
      "lengths": "metres",
      "q": "radians"
    },
    "axes": "Right-handed base; joints rotate about +z, links extend along their rotated local +x.",
    "timestamp_assumptions": "All joint values are one simultaneous static configuration.",
    "batching": "lengths(N,), q(N,), 1<=N<=1000 -> float64 origins(N+1,2), tool_pose(3,3)."
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
    "evaluator_sha256": "8b9225974433929db3e46b931d658bc3c4d1c4a0c99242094d3ae0c74c8f280f"
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
  "summary": "Compute every joint endpoint and the tool pose of a planar serial chain.",
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
  "prerequisite_problem_ids": [],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Compute Forward Kinematics for a Serial Chain

Compute every joint endpoint and the tool pose of a planar serial chain.

```python
def planar_forward_kinematics(lengths, q):
```

## Contract

Lengths must be positive; angles are relative to the preceding link and may lie outside [-pi,pi]. Base origin is [0,0] with identity orientation. Rotate each link by its joint angle before translating along that rotated link by its length. Return the base and all distal endpoints, plus the homogeneous planar transform mapping tool coordinates into the base frame. No joint limits, collisions, or dynamics.

**Shapes and outputs:** lengths(N,), q(N,), 1<=N<=1000 -> float64 origins(N+1,2), tool_pose(3,3).

**Units:** lengths: metres, q: radians. **Time:** All joint values are one simultaneous static configuration.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,0.5], q=[pi/2,-pi/2]` â†’ origins `[[0,0],[0,1],[0.5,1]]`, tool pose `[[1,0,0.5],[0,1,1],[0,0,1]]` up to roundoff.
2. `lengths=[2], q=[0]` â†’ origins `[[0,0],[2,0]]`, tool pose `[[1,0,2],[0,1,0],[0,0,1]]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
