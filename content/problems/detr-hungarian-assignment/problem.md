# Match Object Queries with the Hungarian Algorithm

Implement match_queries(cost). cost is a finite NumPy float64 array (Q,M),1<=Q<=128,0<=M<=Q, abs values<=1e6. Return new NumPy int64 query_for_target(M,): each target j gets one query index in[0,Q), all selected query indices distinct, minimizing sum(cost[query_for_target[j],j]). Any globally optimal assignment is accepted when costs tie; do not assume a lexicographic tie requirement. Empty targets return shape(0,). Preserve inputs and support noncontiguous arrays. TypeError for non-array cost; ValueError for other violations. Implement a polynomial assignment algorithm using Python/NumPy; SciPy is not installed. Target order is preserved; unused queries are not returned. Costs are dimensionless matching objectives for one image, not probabilities or timestamps. Optimal objective comparisons use atol1e-7,rtol1e-9; index validity is exact.

## Worked examples

## Greedy matching can fail

cost=[[1,2],[2,100]], float64. Return [1,0], with total2+2=4. Choosing query0 for target0 greedily would force target1 to pay100, total101.

## More queries than targets

cost=[[4,1],[1,5],[3,3]], float64. Return [1,0], total1+1=2. Query2 is unused. For an all-zero2x2 matrix either [0,1] or [1,0] is accepted.

## Hints

1. Think of targets as rows to be assigned to distinct query columns.
2. An augmenting path may replace earlier matches.
3. Maintain minimum reduced-cost slack for unreached queries; do not enumerate permutations.
