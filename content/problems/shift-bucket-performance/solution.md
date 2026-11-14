# Solution explanation

Use bucket counts and weighted sums for the mean; scatter maximum errors for worst-case loss. Initialize unobserved estimates as NaN and only divide where the count is positive. Work O(N+B), storage O(B) plus output, preserving every input array.
