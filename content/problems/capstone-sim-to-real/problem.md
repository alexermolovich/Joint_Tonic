# Evaluate Sim-to-Real Release Evidence

Implement `sim_to_real(success, observed, latency, seed, min_rate, max_gap, budget_ms)`.

Generate deterministic stratified simulation factors and compare synthetic simulator, replay, shadow, and real-domain evidence.

`success` and `observed` are bool `(N,4)`, with columns in exactly simulator/replay/shadow/real order, `4<=N<=1024`. Success values at unobserved slots are ignored. Rows identify independently sampled scenario trials; repeated observations from one physical episode would violate the statistical assumption. Each row has one factor assignment shared across all four domains. The data are supplied synthetic outcomes, not an actual simulator or real-robot run. `latency` float64 `(N,4)` is milliseconds `[0,10000]` and is also ignored where unobserved after finite/range validation. `seed` is exactly int in `[0,2**32-1]`.

Generate `u=np.random.Generator(np.random.PCG64(seed)).random((N,2))` once. Stratum `s=i%4` at row i combines friction half `s//2` and lighting half `s%2`. Friction is `0.4+0.4*(s//2+u[i,0])`, a dimensionless coefficient; lighting gain is `0.5+0.5*(s%2+u[i,1])`, dimensionless. This stratifies the four joint-factor buckets with counts differing by at most one. It versions a simple synthetic distribution, not the complete paper randomization model.

Return `factors` fresh float64 `(N,2)`, `strata` int64 `(N,)`, `counts` int64 `(4,4)` indexed bucket/domain, `rates` float64 `(4,4)` success fractions (NaN when missing), `mean_rate` float64 `(4,)`, `worst_rate` float64 `(4,)` minimum among observed bucket rates (NaN if no observations), `p95_ms` float64 `(4,)` nearest-rank observed latency (NaN when none), and `wilson` float64 `(4,2)` lower/upper two-sided Wilson intervals for total observed Bernoulli trials per domain, using z=1.959963984540054. Empty domains have both endpoints NaN. `sim_real_gap` float64 `(4,)` is simulator rate minus real rate in each bucket, NaN unless both observed.

`min_rate,max_gap` are Python int/float in `[0,1]`, `budget_ms` in `[0,10000]`. `decision` is `promote` only if **every bucket/domain** has at least two observations, real-domain Wilson lower endpoint is >=min_rate, every bucket's sim-real gap <=max_gap (improvements are allowed), and real-domain p95<=budget_ms; otherwise `hold`. No failure/unknown value is silently filled with zero. Also return `distribution_sha256`: SHA256 hex of the ASCII canonical JSON (`sort_keys=True`, compact separators) of exactly `{schema:1,seed:seed,samples:N,friction:[0.4,1.2],lighting:[0.5,1.5],strata:4}`. The fingerprint identifies this declared distribution and generator seed; supplied outcomes require separate provenance in Notes. Runtime O(N log N), bounded memory O(N).


## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

### Example 1: complete synthetic evidence

Use eight rows, all successes and observed, every latency 5 ms, seed 7, minimum rate 0.5, maximum gap 0.2, and budget 10 ms. Strata are `[0,1,2,3,0,1,2,3]`, counts are all 2, rates/means/worst rates are all 1, p95 is 5 ms, gaps are zero. Wilson intervals are approximately `[0.675592,1]` for each domain; decision is `promote`. The first factor pair is approximately `(0.650038,0.948607)`.

### Example 2: a hidden transfer failure

Set real-domain success False at rows 0 and 4. Real overall rate is 0.75, but bucket-zero real rate is 0 and its sim-real gap is 1. Decision is `hold`, even though the other three buckets all succeed. This failure must appear in the evidence report.

## Source and scope

[Primary source](https://arxiv.org/abs/1703.06907). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
