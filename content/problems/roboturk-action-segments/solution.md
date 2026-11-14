# Solution explanation

Promote actions to float64 without rejecting nonfinite anomaly evidence. Build independent corruption and valid-near-zero masks, then scan maximal contiguous candidate runs. Subtract integer timestamps at the first and last observed samples, and retain only runs meeting both count and duration thresholds. Return fresh flags and Python-int segment tuples. Work O(TD), storage O(TD+T) for the simple promoted-array implementation.
