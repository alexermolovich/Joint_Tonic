## Approach

Check the sample count before allocating. Convert each input to a NumPy array, reject unsupported dtypes and shape, then convert to float64 and validate finite values and the seven inclusive joint limits. Build `N` fractions over `[0,1]`, reshape to `(N,1)`, and blend the two endpoint vectors through broadcasting.

The result has shape `(N,7)` with independent storage. At fractions zero and one it recovers the endpoints; a stationary endpoint pair produces identical rows. Do not normalize angles or clip invalid inputs: neither is part of this joint-coordinate contract.

Time and output space are $O(7N)$. The existing isolated evaluator grades array values and validation; the separate MuJoCo process receives only the bounded public demonstration result for kinematic rendering.
