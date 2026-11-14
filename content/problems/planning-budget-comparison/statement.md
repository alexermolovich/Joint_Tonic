# Compare Path Cost Across Sampling Budgets

Implement `compare_budgets(budgets, costs, observed, solved)`.

Compare cumulative incumbent path costs across increasing sampling budgets, preserving missing observations.

`budgets` is int64 `(B,)`, `1<=B<=128`, strictly increasing positive sample counts at most 1e9. `costs` is nonnegative float64 `(S,B)`, `1<=S<=256`. `observed` and `solved` are bool `(S,B)`; solved must imply observed. Rows are paired fixed seeds across budget columns; all costs use the same normalized path-cost units. Entries not marked solved are finite nonnegative placeholders and are ignored numerically.

Validate the cumulative incumbent contract per seed across the entire row, including across missing columns: once solved, every later observed entry must be solved, and successive observed solved costs must not increase. Missing columns do not reset this state.

Return a dictionary: int64 `counts (B,)` number observed; float64 `success_rate (B,)` solved/observed or NaN if no observation; float64 `median_solved_cost (B,)` median over solved seeds or NaN if none; int64 `paired_counts (B-1,)` number solved at both adjacent budget columns; float64 `paired_improvement (B-1,)` mean previous-cost minus next-cost over those pairs, or NaN if none. Do not impute missing results or compare different seeds as pairs. One budget yields empty paired arrays. This diagnostic summarizes finite experiments, not an asymptotic optimality proof.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Budgets `[10,20]`, costs `[[5.,3.],[0.,4.]]`, all observed, solved `[[True,True],[False,True]]` yield counts `[2,2]`, success rate `[0.5,1.]`, median solved cost `[5.,3.5]`, paired counts `[1]`, paired improvement `[2.]`.
2. Budgets `[10,20]`, one row of zero placeholder costs, both masks all False yield counts `[0,0]`, NaN rates/medians, paired count `[0]` and NaN improvement.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
