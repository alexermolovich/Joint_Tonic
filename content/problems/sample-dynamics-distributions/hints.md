# Hints

1. Validate draw columns and all four bounds before transforming any values, including for B=0.
2. Work in log space for positive scales, and count both endpoints when computing the number of integer delay choices.
3. Keep delay_ticks int64. Convert to seconds using the control interval, then return separate typed arrays.

Do not create a new RNG inside the function. The input draws are the entire deterministic sampling state.
