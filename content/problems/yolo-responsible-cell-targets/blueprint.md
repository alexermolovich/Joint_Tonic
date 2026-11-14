---
{
  "schema_version": 1,
  "problem_id": "yolo-responsible-cell-targets",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Assign Ground-Truth Objects to Responsible Cells",
  "summary": "Build one ground-truth target per YOLO-v1 grid cell with an explicit crowded-cell policy.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "yolo-v1",
    "yolo-responsible-cell-targets"
  ],
  "paper_ids": [
    "2016-yolo-v1"
  ],
  "paper_sections": [
    "Unified detection grid and training objective; downstream evaluation teaching protocol explicitly distinguished"
  ],
  "track_ids": [
    "paper-2016-yolo-v1"
  ],
  "prerequisite_problem_ids": [
    "decode-yolo-grid"
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
  "entrypoint": "solution.assign_yolo_cells",
  "physical_contract": {
    "frames": [
      "Normalized image x-right y-down; grid row=y"
    ],
    "units": {
      "values": "image fractions and grid indices"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "7e12930cf016aa1284d0fc1d796a8d1d76bacf0dc3125c224323c7b6cbb8cf74"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1506.02640"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Assign Ground-Truth Objects to Responsible Cells

Implement `assign_yolo_cells(boxes: np.ndarray, labels: np.ndarray, grid_size: int, num_classes: int) -> dict`.

Build one ground-truth target per YOLO-v1 grid cell with an explicit crowded-cell policy.
boxes float64(N,4) is normalized (cx,cy,width,height),0<=N<=4096. Centers are in [0,1),sizes in (0,1]. labels int64(N,) are in [0,num_classes). grid_size S is built-in int1..64,num_classes built-in int1..256 (neither bool). Cell(row,col)=(floor(cy*S),floor(cx*S)). If multiple objects share a cell, keep greatest width*height; exact area ties keep smaller original object index. Return dict object_indices int64(S,S), class_ids int64(S,S), box_targets float64(S,S,4). Empty cells have indices/class -1 and exact zero box target. Occupied targets store (cx*S-col,cy*S-row,width,height). No clipping, predictor-IoU responsibility selection or batch dimension. Largest-area tie handling is an original deterministic teaching policy, not a guarantee that YOLO can represent crowded cells.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Box `[0.75,0.25,0.2,0.4]`,label2,S=2,C=3 occupies row0,col1; its target is `[0.5,0.5,0.2,0.4]`. All other cells remain -1/zero.
2. Boxes `[0.1,0.1,0.2,0.2]` and `[0.2,0.2,0.4,0.4]` both fall in cell(0,0) for S=2. Object1 wins by area0.16 versus0.04.

## Source and scope

[Primary source](https://arxiv.org/abs/1506.02640). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Allocate the target grid and visit objects once, retaining the best candidate per cell. O(N+S²) time/storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
