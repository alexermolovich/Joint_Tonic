# Worked examples

### Example 1: one observed object

Use one true mask pixel, depth `[[1.]]`, score `[1.]`, latency `[5.]`, identity K and transform, zero previous grid, and thresholds `(0.5,10,0,False)`. The centroid is `(0,0,1)` meters, validity is `[True]`, BEV row 2/column 2 is `0.5` with all other cells zero, p95 is 5 ms, invalid fraction is 0, and decision is `promote`.

### Example 2: lost depth on an active release

Change the same depth to zero and `active=True`. All centroid entries are NaN, validity is `[False]`, BEV is zero, invalid fraction is 1, and decision is `rollback`. Latency still reports 5 ms; fast missing evidence cannot pass the gate.
