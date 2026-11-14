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
