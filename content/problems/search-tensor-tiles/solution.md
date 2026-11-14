# Solution explanation

Enumerate candidate triples. Compute the exact integer working-set footprint and discard candidates above the byte budget. Compute padded tile count and the declared toy cost; compare the entire (cost, footprint, tm, tn, tk) key. Return None if nothing fits. Work O(C), extra storage O(1).
