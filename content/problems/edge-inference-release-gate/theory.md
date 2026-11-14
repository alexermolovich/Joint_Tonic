# Release decisions need complete evidence

## Intuition

A model must fit the device and the operating scenario. Mean accuracy can conceal a bad lighting slice; mean latency can conceal deadline misses. A release decision should show each failed rule, so an operator can explain whether the problem is quality, performance, capacity or missing evidence.

## Measurement mathematics

For N included sequential samples with latency ℓ_i in milliseconds and correctness indicator c_i, compute:

$$
A=\frac1N\sum_i c_i,\qquad
Q=\frac{1000N}{\sum_i\ell_i}.
$$

Q is requests per second for this sequential measurement contract. It is not the sum or mean of per-request throughput.

For sorted latencies x_0…x_(N−1), a linear quantile at fraction p uses h=(N−1)p, j=floor(h), and fractional part f:

$$
q_p=(1-f)x_j+fx_{\min(j+1,N-1)}.
$$

Two samples [10,20] give p99=19.9, not 20 under the specified interpolation convention. A tiny sample count is still weak evidence, so min_samples is a separate gate.

For a baseline slice accuracy A_s^old and measured A_s^new, the drop is:

$$
\Delta_s=A_s^{\text{old}}-A_s^{\text{new}}.
$$

Compare Δ_s to an allowed absolute drop in accuracy units, not a relative percentage. The declared 1e−12 tolerance avoids treating binary representation error at an equality boundary as a regression.

## Visual lesson

The benchmark visual displays a latency distribution with p50/p90/p99 markers and an accuracy-versus-latency scatter view. Selecting hardware shows a gate table with threshold, observed value and pass/fail text. Slice rows expose missing evidence. Every chart has a numerical table alternative.

## Worked example

For 10 and 20 ms, total measured service time is 30 ms. Throughput is 2000/30≈66.667 queries per second. Averaging 100 and 50 would incorrectly yield 75. At a p99 ceiling of 19, the release fails even though average latency is only 15.

## Why this matters on a robot

A different robot computer can have a different thermal envelope, accelerator and memory budget. Grouping by hardware prevents fast devices from hiding slow ones. Warmup, invalid records, quality criteria, preprocessing and evaluator versions belong in the benchmark manifest.

## Failure modes and scope

Ignoring missing slices rewards incomplete evidence. Reporting only the first failed rule slows incident response. Comparing hardware in one pooled percentile can hide operational failures.

The [MLPerf Inference paper](https://arxiv.org/abs/1911.02549) motivates controlled scenarios and joint quality/performance constraints. [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) motivates explicit readiness tests. This lesson's gate policy is an original reduced contract, not a safety certification.
