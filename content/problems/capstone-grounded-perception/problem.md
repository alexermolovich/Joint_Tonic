# Build a Grounded Robot Perception Pipeline

Implement `grounded_perception(masks, depth, scores, latency, K, world_from_camera, previous, min_score, budget_ms, max_invalid, active)`.

Fuse supplied phrase-mask predictions into a calibrated occupancy map and evaluate a synthetic perception release.

`masks` is bool `(N,H,W)`, `depth` float64 `(H,W)` in optical-camera meters, `scores` float64 `(N,)` in `[0,1]`, `latency` float64 `(N,)` in milliseconds per query. This gate measures query latency, not complete-frame or end-to-end pipeline latency. Require `1<=N<=64`, `1<=H,W<=64`, depth in `[0,100]`, latency in `[0,10000]`. `K` float64 `(3,3)` is exactly `[[fx,0,cx],[0,fy,cy],[0,0,1]]`, with `1e-3<=fx,fy<=1e4`. `world_from_camera` float64 `(4,4)` is a rigid transform: final row `[0,0,0,1]`, orthonormal proper rotation within absolute tolerance `1e-9`, translation in meters. Optical axes are right/down/forward; the world is right-handed with x/y defining the map plane. `previous` float64 `(4,4)` contains nonnegative prior occupancy counts. Arrays describe one synchronized frame; previous counts are already aligned to that world grid. No camera calibration estimation or time alignment occurs here.

`min_score` is a Python int/float in `[0,1]`; `budget_ms` in `[0,10000]`; `max_invalid` in `[0,1]`; `active` is exactly bool. For every query with score at least `min_score`, intersect its mask with strictly positive depth pixels. If none remain, reject it. Unproject **each** retained pixel center `(column,row)` using its depth, transform to world, and average the world points. Grid column is `floor(x+2)`, row `floor(y+2)`: four one-meter cells on each axis cover `[-2,2)` meters. Reject centroids outside this grid. Overlapping query masks remain independent observations; no deduplication is implied.

Return a dict with `centroids`: fresh float64 `(N,3)` world positions (all-NaN rows for rejected queries), `valid`: bool `(N,)`, `bev`: float64 `(4,4)` equal to `0.5*previous+0.5*current_counts`, `p95_ms`: Python float using nearest rank `ceil(0.95*N)`, and `invalid_fraction`: fraction rejected **among score-eligible queries** (1 if none eligible). Gate passes iff at least one query is valid, invalid fraction `<=max_invalid`, and p95 latency `<=budget_ms`. `decision` is `promote` on pass, otherwise `rollback` when active and `hold` when inactive. Invalid masks/depth are failure evidence; malformed array contracts raise ValueError. This consumes synthetic model outputs, not Grounding DINO/SAM inference. Time O(NHW), memory O(NHW).


## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

### Example 1: one observed object

Use one true mask pixel, depth `[[1.]]`, score `[1.]`, latency `[5.]`, identity K and transform, zero previous grid, and thresholds `(0.5,10,0,False)`. The centroid is `(0,0,1)` meters, validity is `[True]`, BEV row 2/column 2 is `0.5` with all other cells zero, p95 is 5 ms, invalid fraction is 0, and decision is `promote`.

### Example 2: lost depth on an active release

Change the same depth to zero and `active=True`. All centroid entries are NaN, validity is `[False]`, BEV is zero, invalid fraction is 1, and decision is `rollback`. Latency still reports 5 ms; fast missing evidence cannot pass the gate.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
