# Differentiate Rendered Color on a Small Synthetic Field

## Intuition

Increasing one sample's density makes its own color more visible and hides everything behind it. The gradient must account for both effects, including background. Differentiating only the local opacity misses the occlusion mechanism that trains a radiance field.

## Mathematics and physical meaning

For batch ray $b$ and ordered sample $i$, density $\sigma_i$ has units $\mathrm m^{-1}$, interval $\delta_i$ is meters along a unit-direction ray, and color $c_i\in[0,1]^3$ is linear RGB. Define optical thickness $\tau_i=\sigma_i\delta_i$, opacity $\alpha_i=1-e^{-\tau_i}$ and transmittance
$$T_i=\exp\left(-\sum_{j<i}\tau_j\right),\quad w_i=T_i\alpha_i,\quad C=\sum_iw_ic_i+T_{\mathrm{end}}c_{\mathrm{bg}}.$$
Here $T_{\mathrm{end}}$ includes every interval and the background is one shared RGB vector. With target $y_b$ and $B$ rays, the scalar loss and its color derivative are
$$L=\frac{1}{3B}\sum_b\|C_b-y_b\|_2^2,\qquad g_b=\frac{2(C_b-y_b)}{3B}.$$
Let $R_i=\sum_{k>i}w_kc_k+T_{\mathrm{end}}c_{\mathrm{bg}}$ be the downstream RGB contribution. Then
$$\frac{\partial L}{\partial c_i}=w_i g_b,\qquad \frac{\partial L}{\partial\sigma_i}=g_b^\top\delta_i(T_{i+1}c_i-R_i).$$
The color gradient has shape $(B,S,3)$ and density gradient $(B,S)$; density-gradient units are meters times squared RGB units. Inputs do not include field-network parameters, so no MLP parameter gradient is requested. Near opacity zero, `-expm1(-tau)` avoids cancellation; full opacity can underflow transmittance consistently to zero.

## Visual trace

| One red sample, black target/background | Value |
|---|---:|
| Density / interval | `log(2)` / `1 m` |
| Opacity / surviving transmittance | `.5 / .5` |
| Rendered red | `.5` |
| Mean RGB squared error | `1/12` |
| Density gradient | `1/6` |
| Red color gradient | `1/6` |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** One ray/sample has density `0`, interval `1`, red sample color `[1, 0, 0]`, and black target/background. Output RGB is `[0, 0, 0]`, loss `0`, and both gradient arrays are zero.

**Example 2.** Replace density by `log(2)`. Output RGB is `[.5, 0, 0]`, loss `1/12`, density gradient `1/6`, and color gradient `[1/6, 0, 0]`, with original batch/sample dimensions retained.

## Why this matters on a robot

Differentiable rendering connects image errors to a robot's learned scene representation. Ignoring background attenuation gives wrong gradients even for an empty-looking ray. A low RGB loss does not alone establish correct metric geometry or collision safety.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2003.08934). This explanation, table and code are original.

- [nerf hierarchical depth sampling](/problems/nerf-hierarchical-depth-sampling)
