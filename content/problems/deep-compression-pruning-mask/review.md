# Independent review and runtime verification

Status: reviewed and implemented. Author: curriculum_continuation. Contract reviewer: root. Independent reference, cases and theory reviewer: perception_completion.

Review confirmed channel-axis reductions, equivalent scaling, int8 ties-to-even rounding with int64 accumulation, per-row error gates, inclusive pruning masks, supplied-centroid tie ordering, exact Kraft feasibility and separate stream rounding, correlated activation-output errors, and groupwise affine rounding order with a positive float64 scale floor. Numerical/shape traces are original and distinguish bounded recipes from full paper or kernel reproduction. Easy ratings apply to the three single-core-operation tasks.

Actual isolated bubblewrap verification across this nine-problem batch: 18 public Run families and 45 full Submit families passed. All nine starters and nine plausible mechanism mutants were rejected. Mutants exercised wrong reduction, wrong rescaling, narrow integer accumulation, equality gates, signed pruning, last-centroid ties, missing sparse-index budget, weight-only selection, and rounding after zero-point addition. Cases include independent scalar oracles at realistic scale, noncontiguous arrays, float32-to-float64 promotion, invalid documented inputs, input preservation, empty vectors where supported, and subnormal group scales. All 67 inline/display equations across the nine Theory notes render with strict KaTeX.

Pinned local runtime: Python3.12.3, NumPy2.2.4, bubblewrap;18s wall,10s CPU,4096MiB address-space budget,64KiB output,no network. OCI digest remains pending; these native-local contracts are not automatically production-qualified. No worker code changes.
