# The robot pose belongs to the image's time

## Intuition

A camera and joint encoder rarely sample at identical rates. Pairing an image with the most recently received state can put the robot geometry at the wrong pose, especially when messages have different transport delays. Alignment should use measurement timestamps, not the order packets reach the application.

This lesson assumes the clocks are already synchronized. Source times $t_i$ are strictly increasing seconds; $q_i\in\mathbb R^D$ contains D joint positions in radians. Angles have already been unwrapped, so an ordinary difference describes the intended motion rather than crossing a representation discontinuity at $\pm\pi$.

## Interpolating between measurements

For query time $t$ bracketed by $t_i<t<t_{i+1}$, define:

$$
\lambda=\frac{t-t_i}{t_{i+1}-t_i},\qquad
q(t)=(1-\lambda)q_i+\lambda q_{i+1}.
$$

The weight is dimensionless. The same weight applies to every joint channel, preserving one simultaneous robot configuration. This local model assumes approximately constant joint velocity over the interval.

An exact recorded timestamp returns its measurement directly. A query outside the source range has no two-sided evidence, so this contract marks it invalid rather than extrapolating motion. A long internal gap is also invalid when:

$$
t_{i+1}-t_i>\Delta_{max},
$$

where $\Delta_{max}$ is the caller's allowed gap in seconds. Equality is accepted. These rules separate an estimated value from whether the available evidence supports that estimate.

## Worked sensor example

At times 0 and 1 seconds, two-joint states are $(0,2)$ and $(2,0)$. At camera time 0.25 seconds, the interpolation weight is 0.25 and the aligned state is $(0.5,1.5)$. A query at 0.75 yields $(1.5,0.5)$. Both joints use the same time fraction.

## Visual and diagnostic plan

The planned view places camera exposures above joint-state traces. Selecting an exposure highlights its bracketing samples, weights, and gap. A table supplies query time, left/right timestamps, estimate, and validity reason. Missing intervals are shaded instead of visually suggesting a trustworthy continuous signal.

## Why it matters and what can fail

A small timing error during fast motion can resemble an extrinsic calibration error. Interpolation cannot correct a biased clock or reconstruct unobserved acceleration. Linear interpolation also does not remove encoder noise; it combines neighboring noisy observations and may introduce correlation between aligned examples. Record clock source, synchronization method, gap policy, and unwrapping version with the dataset. Avoid silently treating an invalid row as a real zero-angle configuration.
