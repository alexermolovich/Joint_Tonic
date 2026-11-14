# Solution explanation

Convert values to float64, validate bounds and scalar types, then form nonnegative interval distance. Handle zero margin using a Boolean membership mask. For positive margin, suppress division overflow, cap the ratio, square and exponentiate. Work and storage O(N).
