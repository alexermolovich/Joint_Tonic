# Solution explanation

Shrink the allowed box by its margins, intersect with requested bounds, and check nominal inclusion. A reversed intersection or excluded nominal value is infeasible and gets NaN output bounds. Do not repair a failed box by swapping endpoints. Work/storage O(D).
