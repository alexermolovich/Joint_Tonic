# Solution explanation

Compare each candidate against all others using weak improvement on both metrics and strict improvement on at least one. Equal-metric models remain on the frontier. Independently filter feasible models, then minimize (-accuracy, latency, ID). Work O(N²), storage O(N), bounded at 1000 candidates.
