# Solution explanation

Handle an empty token axis explicitly. Select maxima over valid entries, give all-missing rows a safe arithmetic maximum, exponentiate masked scores and divide only where the weight sum is positive. Work/storage O(BL), no overflow from positive exponents.
