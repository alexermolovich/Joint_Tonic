---
{
  "schema_version": 1,
  "problem_id": "trace-perception-frame-graph",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Trace Frames Through a Robot Perception Graph",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.resolve_frame_transform",
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
      "named right-handed frames in supplied forest"
    ],
    "units": {
      "translation": "metres",
      "rotation": "dimensionless"
    },
    "axes": "An edge (parent,child,T) stores T_parent_child mapping child coordinates into parent.",
    "timestamp_assumptions": "Every edge belongs to the same synchronized calibration snapshot; no time interpolation.",
    "batching": "list of up to128 (parent:str,child:str,T(4,4)) tuples, source/target str -> fresh float64(4,4)."
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
    "evaluator_sha256": "119a023f63bdc51c5b65ea9bb515908e16729b8f978ab4b19e1da1ad23443250"
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
  "summary": "Resolve a rigid transform between two frames in a validated acyclic frame forest.",
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
  "prerequisite_problem_ids": [],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Trace Frames Through a Robot Perception Graph

Resolve a rigid transform between two frames in a validated acyclic frame forest.

```python
def resolve_frame_transform(edges, source, target):
```

## Contract

Frame names match ASCII [a-z][a-z0-9_]{0,31}. Each child has at most one parent; reject cycles, self-edges, repeated children, and malformed transforms even in disconnected components. Rigid matrices use atol=1e-8 for orthogonality, determinant +1 and bottom row. Both query names must occur in the graph. Return T_target_source along the unique undirected path, inverting edges when needed. Same known source/target returns identity. Disconnected queries raise ValueError. Edges must be a list of tuples of length3.

**Shapes and outputs:** list of up to128 (parent:str,child:str,T(4,4)) tuples, source/target str -> fresh float64(4,4).

**Units:** translation: metres, rotation: dimensionless. **Time:** Every edge belongs to the same synchronized calibration snapshot; no time interpolation.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. Let T_base_wrist translate `[1,0,0]` and T_wrist_camera translate `[0,2,0]`. Resolving source="camera", target="base" returns translation `[1,2,0]` with identity rotation.
2. Reversing those query frames returns translation `[-1,-2,0]`. A known frame to itself returns identity.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

For every (parent,child,T) edge, T maps homogeneous child-frame points into the parent frame: p_parent=T@p_child.
