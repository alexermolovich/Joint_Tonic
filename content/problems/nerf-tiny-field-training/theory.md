# Fit a Tiny Coordinate-Feature Radiance Field

## Intuition

A radiance field is useful because one shared function describes all sampled locations. Rendering turns its density and color outputs into image predictions; image error then trains the shared function. Here the function is deliberately small: an affine map of supplied coordinate features. You can inspect every gradient and update without training the paper's deep, view-dependent model.

## Field and coordinate contract

Each sample has a fixed feature vector $x\in\mathbb R^F$ from the same scene coordinate convention. Features are dimensionless; this exercise receives them and does not generate camera rays or Fourier features. Weight $W\in\mathbb R^{F\times4}$ and bias $b\in\mathbb R^4$ are shared across all rays and samples:
$$r=xW+b,\qquad \sigma=\log(1+e^{r_0}),\qquad c_j=\operatorname{sigmoid}(r_{j+1}),\quad j=0,1,2.$$
The fixed density scale is one inverse meter, so optical thickness is dimensionless when multiplied by a metric interval. Colors and targets are linear RGB. Training features have shape $(B,S,F)$ and evaluation features $(R,S,F)$: ray counts $B,R$, sample count $S$, feature width $F$.

## Render and differentiate

For metric interval $\delta_i$, define $\tau_i=\sigma_i\delta_i$, $T_i=\exp(-\sum_{k<i}\tau_k)$, $\alpha_i=1-e^{-\tau_i}$ and $w_i=T_i\alpha_i$. Background $c_{\mathrm{bg}}$ is shared across rays. Render and loss are
$$C=\sum_i w_ic_i+T_{\mathrm{end}}c_{\mathrm{bg}},\qquad L=\frac1{3B}\sum_{q=1}^B\|C_q-y_q\|_2^2.$$
Here $y_q$ is the training target and $T_{\mathrm{end}}$ includes every interval. The RGB derivative is $g_q=2(C_q-y_q)/(3B)$. The downstream contribution $D_i=\sum_{k>i}w_kc_k+T_{\mathrm{end}}c_{\mathrm{bg}}$ gives
$$\frac{\partial L}{\partial\sigma_i}=g_q^\top\delta_i(T_{i+1}c_i-D_i),\qquad \frac{\partial L}{\partial c_i}=w_i g_q.$$
Use the chain rule through the field activations:
$$a_{i,0}=\frac{\partial L}{\partial\sigma_i}\operatorname{sigmoid}(r_{i,0}),\qquad a_{i,j+1}=\frac{\partial L}{\partial c_{i,j}}c_{i,j}(1-c_{i,j}).$$
The vector $a_i\in\mathbb R^4$ is the raw-field gradient. Sum over every training ray/sample:
$$G_W=\sum_{q,i}x_{qi}^{\top}a_{qi},\qquad G_b=\sum_{q,i}a_{qi}.$$
The outer product produces $(F,4)$, while the bias gradient has shape $(4,)$. The MSE normalization already appears in $g_q$; do not divide these sums by batch size again.

## Clipped simultaneous updates

Record the raw global gradient norm $n=\sqrt{\|G_W\|_F^2+\|G_b\|_2^2}$. For learning rate $\eta$, update both parameters from the same old state:
$$W\leftarrow W-\eta G_W/\max(1,n),\qquad b\leftarrow b-\eta G_b/\max(1,n).$$
The clip is a declared teaching policy, not NeRF's released optimizer recipe. Record training loss before the first update and after each update. Evaluate held-out rays only after the last update; evaluation targets never determine gradients, clipping, stopping or model selection. Fixed step count does not promise monotone loss reduction on every allowed input.

## Visual execution trace

| Stage | Shape | Meaning |
|---|---|---|
| Supplied training features | B,S,F | Fixed scene coordinates in a shared feature basis |
| Shared affine field | B,S,4 | Density logit and three color logits |
| Positive density and bounded color | B,S and B,S,3 | Metric attenuation and linear RGB |
| Ordered volume compositing | B,3 | Training image prediction |
| Analytic chain rule | F,4 and 4 | One shared parameter gradient |
| Global clip and SGD | F,4 and 4 | New field parameters |
| Held-out render | R,3 | Evaluation only |

This static pipeline table is the text alternative; no animation is needed.

## Worked update

Use one ray, sample and feature, feature value 1, interval 1 meter, zero initial weight/bias, and black target/background. Density is $\log2$, opacity $1/2$, color $1/2$ in every channel and rendered RGB $1/4$. The mean RGB loss is $1/16$. The raw density gradient is $1/16$ and each raw color gradient is $1/48$. Weight and bias have the same gradient, so $n=\sqrt{1/96}<1$.

With learning rate $0.1$, the new weight row and bias both equal $[-1/160,-1/480,-1/480,-1/480]$. The next density logit is $-1/80$ and each color logit is $-1/240$. This concrete trace checks background-aware rendering, batch normalization and simultaneous updates.

For a zero-error example, use the same initial field but set target and background to $[.5,.5,.5]$. The rendered RGB is exactly that same value; all gradients remain zero and any allowed number of updates leaves parameters unchanged.

## Why this matters on a robot

Shared scene representations can connect observations from multiple viewpoints, but a small image loss is not proof of metric geometry or collision-free free space. Incorrect interval units change density learning; ignoring background attenuation changes gradients; training on evaluation targets hides generalization failures. This bounded exercise omits view-dependent appearance, a deep MLP, coarse/fine resampling, pose optimization and full-scene reconstruction.

## Sources and prerequisites

[NeRF primary paper](https://arxiv.org/abs/2003.08934). Original explanation, code, table and synthetic fixtures.

- [Coordinate Fourier features](/problems/nerf-fourier-features).
- [Volume color/depth rendering](/problems/nerf-render-color-depth).
- [Analytic rendered-color gradients](/problems/nerf-rendered-color-gradients).
- [Hierarchical depth sampling](/problems/nerf-hierarchical-depth-sampling) is an optional extension; this task uses fixed supplied intervals.
