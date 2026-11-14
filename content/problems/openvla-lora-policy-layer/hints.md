# Hints

1. Apply the frozen base weight to x without detaching x or the complete base result.
2. Compute the low-rank branch through the rank-r hidden width, then scale by alpha/r.
3. Keep both adapter branches in the graph when their current output or derivative is zero.
