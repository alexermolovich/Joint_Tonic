# Track Policy Version Staleness

## Contract

`policy_staleness_report(current_version, sample_versions, sample_counts, max_lag) -> dict`. current_version and max_lag are built-in ints in 0..2^63-1. sample_versions and sample_counts are NumPy int64(N,),0<=N<=100000; versions in 0..2^63-1, counts in 0..10^6. Versions newer than current are valid anomaly evidence, not invalid inputs. Return lag:int64(N,)=current-version, future:bool(N,)=lag<0, stale:bool(N,)=lag>max_lag, accepted:bool(N,)=~future & ~stale. Also return Python ints accepted_samples and rejected_samples from the supplied counts, and float mean_known_lag weighted by counts over all nonfuture rows (including stale). If their total count is zero, mean_known_lag=NaN. Use exact integer differences before floating averaging. Version lag is dimensionless, not elapsed time or divergence. Work O(N).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

current=10, versions[10,7,12], counts[2,6,4], max_lag=2 gives lag[0,3,-2], future[F, F, T], stale[F, T, F], accepted[T, F, F], accepted_samples=2, rejected_samples=10, mean_known_lag=18/8=2.25.

current=0, versions[1], counts[5], max_lag=0 gives lag[-1], future[T], stale[F], accepted[F], accepted_samples=0, rejected_samples=5, mean_known_lag=NaN.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
