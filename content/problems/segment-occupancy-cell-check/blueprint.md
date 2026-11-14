---
{
  "schema_version": 1,
  "problem_id": "segment-occupancy-cell-check",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Check a Segment Against Occupancy Cells",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.segment_is_free",
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
      "fixed grid frame with origin at lower-left boundary"
    ],
    "units": {
      "start,end": "metres",
      "grid": "binary occupancy"
    },
    "axes": "x increases with column; y increases with row. Every cell is a 1 metre square.",
    "timestamp_assumptions": "One static occupancy snapshot; obstacles do not move.",
    "batching": "grid(H,W), 1<=H,W<=128, start/end(2,) -> Python bool."
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
    "evaluator_sha256": "b1990616c73eb05524f8d1a3e491c114f3442b338cd7620d4d8d41a542f70432"
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
  "summary": "Check a continuous point-robot segment against closed occupied grid cells, including grazing contact.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "planning-control"
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

# Check a Segment Against Occupancy Cells

Check a continuous point-robot segment against closed occupied grid cells, including grazing contact.

```python
def segment_is_free(grid, start, end):
```

## Contract

Grid contains integer-valued zeros and ones (real numeric dtype; boolean dtype follows the general rejection policy). Endpoints must lie in the closed map rectangle [0,W]x[0,H]. Occupied row r,column c is the closed square [c,c+1]x[r,r+1]. Return False if any point of the closed segment touches/intersects any occupied square; otherwise True. Boundary contact counts as collision. Equal endpoints are valid. Do not use sparse sampling that can skip a thin crossing.

**Shapes and outputs:** grid(H,W), 1<=H,W<=128, start/end(2,) -> Python bool.

**Units:** start,end: metres, grid: binary occupancy. **Time:** One static occupancy snapshot; obstacles do not move.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. In a 3Ã—3 zero grid with grid[1,1]=1, start=[0,1.5], end=[3,1.5] â†’ False.
2. Same grid, start=[0,0], end=[3,0] â†’ True. A segment ending at [1,1] instead returns False because the occupied corner is touched.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Each grid cell has side length exactly 1 metre; x increases with columns and y with rows, with map origin at cell (0,0) lower coordinate corner.
