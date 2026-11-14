# Solution explanation

Compute per-token activation maxima and per-output weight maxima, divide by127 and replace zero scales with1. Apply ties-to-even rounding and clipping to create signed int8 values. Cast both operands to int64 before multiplying, then multiply by the two broadcast scales. Casting an already-overflowed int8 product cannot repair it. Matmul costs O(NCD); quantized arrays and output use O(NC+CD+ND) storage.
