# Integration review

Status: approved for the documented bounded synthetic scope.

- Root reviewed all four contracts and the grounded-perception reference/cases.
- research_curator independently reviewed VLA, edge deployment, and sim-to-real references/cases.
- Fixed the scalar-validation finding: arbitrarily large Python integers are rejected with ValueError before NumPy scalar conversion; all four have regressions.
- Grounded gate uses integer rejected/eligible counts to preserve the inclusive one-third boundary; the input latency is explicitly per-query, not pipeline latency.
- VLA reports only held-out slices; stratified Wilson intervals are labeled approximate descriptive summaries.
- Actual bubblewrap Run and Submit passed; all four starters and null-output mutants rejected. The four integrations cover 31 public+hidden case families total and 8 public Run examples.
- Two plausible mechanism mutants per integration were rejected: transform direction/eligible denominator, gradient scale/training latency leakage, half-open lifetime/preprocessing binding, missing observation/coverage gate.
- Synthetic fixtures are original CC0-1.0. No trained models, source code copies, robot controls, remote deployment, or production keys are included.
