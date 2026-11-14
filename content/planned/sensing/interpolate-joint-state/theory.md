# Joint state at a camera exposure

## Intuition

A camera and an encoder rarely sample at the same instant. Using the latest received joint state can assign a pixel to the wrong robot pose. Interpolation estimates state at the camera's measurement timestamp. It cannot synchronize clocks or remove transport delay.

## One time fraction, several joints

Let $t_i<t_{i+1}$ be bracketing times in seconds and $\mathbf q_i,\mathbf q_{i+1}\in\mathbb R^D$ be already-unwrapped joint angles in radians. For query time $\tau$, define the dimensionless fraction

$$
\alpha=\frac{\tau-t_i}{t_{i+1}-t_i},\qquad
\widehat{\mathbf q}(\tau)=(1-\alpha)\mathbf q_i+\alpha\mathbf q_{i+1}.
$$

For an interior query, $0<\alpha<1$. Each joint uses the same fraction because the channels were sampled together. This assumes approximately constant joint velocity inside the interval. It remains an estimate, not a new sensor measurement.

## Visual: timestamp and shape trace

| Time (s) | 0 | 0.25 | 1 | 1.5 | 2 |
|---|---:|---:|---:|---:|---:|
| Recorded joint 1 (rad) | 0 | — | 1 | — | 2 |
| Query result (rad) | — | 0.25 | — | 1.5 | — |
| Bracket | | 0 to 1 | | 1 to 2 | |

Read left to right: each query sits between two observations. This static table is also the text alternative. Input q has shape (3,2), query weights (2,1), and output (2,2); the extra weight axis broadcasts across joints.

At $\tau=0.25$ s, $\alpha=0.25$. Joint 2 goes from 2 to 4 rad, giving $2+0.25(4-2)=2.5$ rad. The output row is $[0.25,2.5]$.

## Availability before arithmetic

Let $g$ be max_gap in seconds. A non-exact query is valid only if a bracket exists and $t_{i+1}-t_i\le g$. Check exact timestamps first, including the final source timestamp: they need no interpolation.

Invalid rows contain NaN and a false mask. A consumer must inspect the mask before constructing transforms. Returning zero would invent a real joint angle.

## Why this matters on a robot

Interpolating across a long encoder dropout creates false camera-to-tool geometry. Another failure occurs across angular wrap: 179° to −179° interpolates through 0° unless angles were first unwrapped. This contract requires unwrapped inputs.

## Check your understanding

- Why is the sample at 2 s valid in the second example? It was directly observed.
- Can max_gap repair a clock offset? No; the clocks must already agree.

## Source and application

ROS [timestamped cache documentation](https://docs.ros.org/en/rolling/p/message_filters/doc/Tutorials/Cache-Python.html) provides buffering context. The gap/interpolation policy is an original teaching contract. Apply it before [episode validation](/problems/validate-robot-episodes); no paper result is reproduced.
