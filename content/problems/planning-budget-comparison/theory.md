# Compare Path Cost Across Sampling Budgets

## Intuition

A planner may not find a path at every budget, and some runs may be missing entirely. Keep feasibility rates separate from path quality, and compare cost improvements only for the same solved seeds.

## Mathematics and conventions

Let $O_{sb}$ mark observed seed s at budget b, and $F_{sb}$ mark a solved path. With cost $C_{sb}$,

$$n_b=\sum_s O_{sb},\quad r_b=\frac{\sum_sF_{sb}}{n_b}.$$

For adjacent columns define $P_{sb}=F_{sb}F_{s,b+1}$. The paired improvement is

$$g_b=\frac{\sum_s P_{sb}(C_{sb}-C_{s,b+1})}{\sum_sP_{sb}}.$$

Zero denominators produce NaN, not zero. Median cost uses only solved seeds. Budgets are sample counts, and costs/improvements share the supplied normalized path-cost unit. The monotone incumbent rule applies across missing columns too.

## Visual computation trace

| Seed | Budget 10 | Budget 20 | Paired contribution |
| --- | --- | --- | --- |
| A | solved cost 5 | solved cost 3 | improvement 2 |
| B | observed unsolved | solved cost 4 | excluded from cost pair |
| Summary | success 1/2 | success 2/2 | mean improvement 2 |

## Worked examples

1. Budgets `[10,20]`, costs `[[5.,3.],[0.,4.]]`, all observed, solved `[[True,True],[False,True]]` yield counts `[2,2]`, success rate `[0.5,1.]`, median solved cost `[5.,3.5]`, paired counts `[1]`, paired improvement `[2.]`.
2. Budgets `[10,20]`, one row of zero placeholder costs, both masks all False yield counts `[0,0]`, NaN rates/medians, paired count `[0]` and NaN improvement.

## Why this matters on a robot

Ignoring failed searches can make a planner look efficient while hiding poor feasibility. Missing runs must not count as failures or successful zero-cost paths; finite-budget curves also cannot establish an asymptotic theorem.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1005.0416). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
