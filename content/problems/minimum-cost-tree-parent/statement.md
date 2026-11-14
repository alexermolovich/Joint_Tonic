# Choose a Collision-Free Minimum-Cost Tree Parent

Implement `choose_tree_parent(root_costs, edge_costs, feasible)`.

Choose a parent from supplied path-feasible connections by cumulative cost.

`root_costs` and `edge_costs` are float64 `(N,)`, `0<=N<=100000`, nonnegative in one common caller-defined path-cost unit. `feasible` is bool `(N,)`: True means the connecting path has already passed the caller's collision and neighborhood checks, not merely its endpoint. Return a dict `parent`: Python int index minimizing root_cost+edge_cost over feasible candidates, with lowest index breaking exact ties; `total_cost`: Python float of that sum. When no feasible candidate exists, return parent -1 and total_cost positive infinity. This explicit nonfinite output is a missing-parent sentinel; all input costs must still be finite. No coordinates, angular wrapping, timestamps, collision queries or tree mutation occur in this selection step.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Root costs `[3.,1.,2.]`, edge costs `[1.,4.,2.]`, all feasible gives totals `[4.,5.,4.]`: parent0 and total_cost4, using the lower index for a tie.
2. Root costs `[0.,5.]`, edge costs `[0.,1.]`, feasible `[False,False]` returns parent -1 and total_cost +infinity. An infeasible cheap connection cannot become a parent.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
