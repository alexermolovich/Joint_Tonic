# Solution explanation

Subtract versions exactly in int64, classify future and stale rows independently, and sum sample counts under the acceptance mask. Compute the known-lag numerator with Python integer products so large versions multiplied by counts cannot overflow int64. Divide only when known sample count is positive; otherwise return NaN. Work/storage O(N).
