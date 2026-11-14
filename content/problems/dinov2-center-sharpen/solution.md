# Solution

Subtract the supplied center and divide by positive temperature. Subtract each row's maximum, exponentiate, and normalize each row by its own sum. At least one exponent per row is one, preventing a zero denominator even for large score gaps. Complexity is O(BK) time and storage. This neither updates the center nor performs Sinkhorn balancing; those are distinct training operations.
