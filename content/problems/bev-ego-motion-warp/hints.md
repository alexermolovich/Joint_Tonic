# Hints

1. Construct current cell centers, then map them into the previous frame using the supplied direction.
2. Subtract the grid origin and half-cell offset when converting metric positions to fractional array indices.
3. Use floor and four bilinear weights. Check each neighbor before indexing; do not renormalize boundary weights.

