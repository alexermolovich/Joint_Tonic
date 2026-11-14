# Worked examples

current=10, versions[10,7,12], counts[2,6,4], max_lag=2 gives lag[0,3,-2], future[F, F, T], stale[F, T, F], accepted[T, F, F], accepted_samples=2, rejected_samples=10, mean_known_lag=18/8=2.25.

current=0, versions[1], counts[5], max_lag=0 gives lag[-1], future[T], stale[F], accepted[F], accepted_samples=0, rejected_samples=5, mean_known_lag=NaN.
