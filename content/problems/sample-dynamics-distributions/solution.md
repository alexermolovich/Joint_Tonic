# Solution: transform recorded unit draws into physical parameters

Validate the entire draw matrix and all bounds before sampling, including for an empty batch. Each positive physical parameter uses its designated draw column in log space. The equivalent power expression a*(b/a)**u explains why the midpoint is a geometric mean.

The integer delay has hi-lo+1 possible values. Multiply its unit draw by this count, floor, and add lo. Since the input excludes 1, the final bucket cannot exceed hi. Preserve int64 delays in a separate array and multiply them by dt_s to obtain float64 seconds.

All returned arrays are new, and no random state is consumed. Work and storage are O(B). The sampled scalars do not define a complete rigid-body model or a safety-certified parameter envelope; the surrounding simulator must validate those additional physical constraints.
