# Worked examples

### A latency-constrained choice
`select_pareto_model([("fast",.8,2),("accurate",.9,5),("inferior",.7,4)],.75,3)` returns `{"frontier":["accurate","fast"],"selected":"fast"}`.

### Equal metrics retain both IDs
For records[("b",.8,2),("a",.8,2)],min_accuracy.8,max_latency_ms2, return frontier["a","b"] and selected"a".
