# Compare Black-Box and Grey-Box Pipeline Measurements

Implement compare_pipeline_measurements(boundaries, spans) -> list[tuple[str,int,int,int,int]].

boundaries is a Python list of 0–10000 tuples(request_id,start_ns,end_ns), unique request IDs. spans is a list of 0–100000 tuples(request_id,stage_id,start_ns,end_ns), at most one span per(request_id,stage_id). IDs match ASCII [a-z][a-z0-9_-]{0,63}. All timestamps are built-in non-bool ints in [0,2**63-1], start<=end, on the same caller-declared clock. Every span names a known request and lies wholly within its boundary interval. Empty/zero-duration spans are valid.

For each request, return(request_id,boundary_ns,covered_ns,unobserved_ns,overlap_ns) in ASCII request-ID order. boundary_ns=end-start. covered_ns is the length of the union of its half-open spans. unobserved_ns=boundary_ns-covered_ns. overlap_ns is the sum of individual span durations minus covered_ns; triple overlaps count their extra multiplicity. A request without spans has zero coverage and its full boundary duration unobserved. Validate the entire input, preserve it, and raise ValueError for malformed types, duplicate IDs/spans, unknown requests, bounds or inconsistent intervals. All numeric outputs are built-in ints.

Unobserved time is not automatically queue time; overlap is not automatically wasted work. Instrumentation coverage and probe overhead require separate interpretation. No clock synchronization or causal critical-path reconstruction occurs.

## Worked examples

### Overlapping stages
`compare_pipeline_measurements([("r",0,10)],[("r","a",1,6),("r","b",4,8)])` returns `[("r",10,7,3,2)]`.

### No internal evidence
`compare_pipeline_measurements([("r",100,105)],[])` returns `[("r",5,0,5,0)]`.

## Source and scope

This original bounded component is motivated by [2023-robotperf](https://arxiv.org/abs/2309.09212). It does not reproduce the full paper, trained model or benchmark protocol.
