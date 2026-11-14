# Warp a Previous BEV with Ego Motion

## Intuition

A stationary obstacle occupies different grid indices when the robot moves. To align history, visit each current grid cell and ask where that location was in the previous ego frame. This inverse lookup avoids holes that a naive forward scatter can leave.

## Cell centers and frame direction

Let $F\in\mathbb R^{H\times W\times C}$ be the previous feature grid. Row r increases y and column c increases x. The common numerical grid origin is $o=(o_x,o_y)$ metres; resolution $h>0$ is metres per cell. A current cell center is

$$
p_{\mathrm{cur}}(r,c)=
\begin{bmatrix}o_x+(c+\tfrac12)h\\o_y+(r+\tfrac12)h\\1\end{bmatrix}.
$$

The supplied transform $T_{\mathrm{prev}\leftarrow\mathrm{cur}}\in SE(2)$ maps current-frame positions to previous-frame positions:

$$
p_{\mathrm{prev}}=
T_{\mathrm{prev}\leftarrow\mathrm{cur}}p_{\mathrm{cur}}.
$$

Its rotation is dimensionless and translation is in metres. The inverse direction would answer a different question. No perspective divide belongs to this rigid planar transform.

Convert the transformed point back to fractional array indices:

$$
u=(p_{\mathrm{prev},x}-o_x)/h-\tfrac12,\qquad
v=(p_{\mathrm{prev},y}-o_y)/h-\tfrac12.
$$

The half-cell offsets appear once in each direction. Forgetting either one creates a systematic spatial shift.

## Bilinear interpolation with zero extension

Let $i=\lfloor u\rfloor$, $j=\lfloor v\rfloor$, $a=u-i$, and $b=v-j$. Extend F by zero outside its valid integer indices. Then the output feature vector is

$$
G_{rc}=(1-a)(1-b)F_{j,i}
+a(1-b)F_{j,i+1}
+(1-a)bF_{j+1,i}
+abF_{j+1,i+1}.
$$

The weights are dimensionless. Zero extension preserves the fractional contribution of an in-bounds neighbor; renormalizing those weights would change this contract into another boundary rule.

## Visual: one row under a half-cell translation

| Current column | Previous fractional u | Left/right neighbors | Weighted output |
|---:|---:|---|---:|
| 0 | 0.5 | 1 and 2 | 1.5 |
| 1 | 1.5 | 2 and 3 | 2.5 |
| 2 | 2.5 | 3 and 0 (outside) | 1.5 |

This original static sampling trace and text alternative reproduces the first row of example 2. An identity transform samples each cell center exactly and returns equal values in independent storage.

A direct reference needs O(HWC) work and output storage. For very distant coordinates, test neighbor bounds before indexing so negative indices cannot accidentally wrap to the opposite edge.

## Why this matters on a robot

Wrong transform direction can produce a plausible but displaced map, leading temporal fusion to blur stationary obstacles. Resolution mismatch and half-cell errors are similarly systematic. Ego-motion alignment compensates robot motion, not independently moving people or objects. Reset history at episode boundaries and keep timestamp pairing upstream.

## Sources and prerequisites

[BEVFormer](https://arxiv.org/abs/2203.17270) motivates aligning history before temporal reasoning. This original planar grid and zero-padded bilinear contract defines a small testable subcomponent; it does not reproduce the paper's learned temporal attention. Prerequisite: [frame transforms](/problems/se3-transform-points).

