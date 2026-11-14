# Package and Gate an Edge Perception Release

Implement `edge_deployment(latency, quality, drift, sizes, intervals, model_bytes, preprocessing, fixture_key, min_quality, budget_ms, memory_budget, max_drift, active)`.

Select an edge model from measured evidence, reuse tensor buffers, and package a synthetic signed release with a drift gate.

`latency` float64 `(M,R)` contains supplied target-device milliseconds in `(0,10000]`, `quality` float64 `(M,)` and `drift` float64 `(M,)` are `[0,1]`. Require `1<=M<=16`, `1<=R<=128`. Rows identify candidates on the same device/runtime/workload; this function does not benchmark hardware. `sizes` int64 `(M,K)` are requested tensor bytes in `[1,1000000]`, `intervals` int64 `(K,2)` are half-open operation-index lifetimes `[start,end)` with `0<=start<end<=1024`, `1<=K<=64`.

For each model independently, process requests in `(start,index)` order. Reuse a previously allocated buffer iff its last end `<=start` and capacity `>=size`; choose smallest capacity then smallest buffer ID. Otherwise create a new buffer with capacity exactly size. IDs begin at zero in creation order; capacities never change. Return IDs in original request order. `allocated_bytes` is the sum of all buffer capacities, not peak live logical bytes. This conservative persistent arena allocates each reusable buffer once.

Compute per-model p95 latency by sorted nearest rank `ceil(0.95*R)`. Eligible candidates have quality `>=min_quality`, p95 `<=budget_ms`, allocated bytes `<=memory_budget`. `min_quality,max_drift` are Python int/float `[0,1]`, `budget_ms` `[0,10000]`, `memory_budget` exactly int `[1,64000000]`. Choose highest quality, then lowest p95, then lowest index; drift is checked **after** this selection. `active` is exactly bool. If no candidate is eligible or selected drift `>max_drift`, decision is `rollback` if active else `hold`; otherwise `promote`.

`model_bytes` is exactly a list of M bytes objects, each length 1..4096. `preprocessing` is exactly `rgb-0-1` or `bgr-mean`. `fixture_key` is exactly 32 bytes: an intentionally public synthetic HMAC key for this exercise, never a production credential. Return dict `candidate` Python int (-1 if none), `buffer_ids` fresh int64 `(M,K)`, `allocated_bytes` int64 `(M,)`, `p95_ms` float64 `(M,)`, `decision`, `manifest`, `sha256`, and `signature`. If none eligible, the last three are None. Otherwise manifest is canonical ASCII JSON (`sort_keys=True`, `separators=(',',':')`) with exactly `{allocated_bytes: Python int, candidate: Python int, model_sha256: SHA256 hex of selected bytes, preprocessing: string, schema: 1}`. `sha256` hashes its ASCII bytes; `signature` is HMAC-SHA256 hex over those bytes using fixture_key. Package the selected candidate even if the drift gate rejects promotion, so evidence remains inspectable. No timestamps, paths, or ambient keys are used. Time O(MK²+MR log R), bounded memory O(M(K+R)).

This is an original systems integration. Buffer placement and measured selection are executable; model inference, supernet training, production key management and remote deployment are outside its scope.


## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

### Example 1: reuse and select

Use latency `[[4.,5.],[2.,3.]]`, quality `[0.9,0.8]`, drift `[0.1,0.1]`, sizes `[[8,4],[4,4]]`, intervals `[[0,1],[1,2]]`, model bytes `[b'a',b'b']`, preprocessing `rgb-0-1`, key `b'k'*32`, minimum quality 0.8, budget 10 ms, memory budget 8 bytes, max drift 0.2, inactive. Both models reuse buffer zero: IDs `[[0,0],[0,0]]`, allocated bytes `[8,4]`, p95 `[5.,3.]`. Higher-quality candidate 0 is selected and promoted. Its manifest records candidate 0, 8 allocated bytes, SHA256 of `b'a'`, preprocessing, and schema 1.

### Example 2: drift rollback

Change candidate 0 drift to 0.3 and active to True. Candidate 0 and its manifest/signature stay the same, but decision is `rollback`. Candidate 1 is not silently substituted after the selection; the failed release evidence is retained.

## Source and scope

[Primary source](https://arxiv.org/abs/1908.09791). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
