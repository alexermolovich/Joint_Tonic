# Solution explanation

Validate every frequency and length, then test Kraft feasibility with sum(1 << (32-length)) <= 1 << 32. Accumulate weighted code lengths as Python integers. Round symbol and sparse-position streams to whole bytes separately, add the codebook and header, and divide dense float32 bytes by total bytes. Work and storage O(K); no codewords or packed binary artifact are constructed.
