# Solution explanation

Subtract reference from candidate in float64. Reduce squared and absolute errors along output columns to expose the affected token rows. Compare row maxima strictly above the supplied absolute tolerance, while separately computing the guarded global relative norm. Work and intermediate storage O(ND). The relative diagnostic never overrides the documented row gate.
