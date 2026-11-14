# Select a Pareto Model Under Accuracy and Latency Limits

Implement select_pareto_model(records, min_accuracy, max_latency_ms) -> dict.

records is a list of0–1000 tuples(model_id,accuracy,latency_ms), with unique ASCII IDs[a-z][a-z0-9_-]{0,63}. Accuracy and min_accuracy are built-in non-bool int/float finite in[0,1]; latency and max_latency_ms are such numbers in(0,1000000]. All records refer to the same caller-declared workload, quality metric, device and runtime.

A dominates B iff A has accuracy>=B and latency<=B with at least one strict inequality. Return exactly frontier: sorted list of ALL nondominated model IDs across the full input, and selected: the ID of the feasible record with highest accuracy, then lowest latency, then ASCII ID; None if no record meets accuracy>=min_accuracy and latency<=max_latency_ms. Equal metric duplicates with different IDs both remain on the frontier. Threshold equality passes. Validate every record, preserve inputs; malformed contracts raise ValueError. Empty records gives {"frontier":[],"selected":None}.

Frontier membership and feasibility are separate outputs. No FLOP-to-latency conversion, confidence interval or unseen-device prediction occurs.

## Worked examples

### A latency-constrained choice
`select_pareto_model([("fast",.8,2),("accurate",.9,5),("inferior",.7,4)],.75,3)` returns `{"frontier":["accurate","fast"],"selected":"fast"}`.

### Equal metrics retain both IDs
For records[("b",.8,2),("a",.8,2)],min_accuracy.8,max_latency_ms2, return frontier["a","b"] and selected"a".

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
