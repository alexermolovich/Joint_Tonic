# Compute an Exposure-Corrected Photometric Residual

## Intuition

The same scene can have different measured intensity after an exposure change. Correct the predicted brightness before judging mismatch, then limit the influence of large residuals with a robust objective.

## Mathematics and conventions

For source and target intensity samples $I_i,I_j$, exposure times $t_i,t_j$ in seconds, log gains $a_i,a_j$ and offsets $b_i,b_j$ in intensity units,

$$\gamma=\frac{t_j}{t_i}e^{a_j-a_i},\qquad r=I_j-b_j-\gamma(I_i-b_i).$$

For weight $w\in[0,1]$ and intensity threshold $\delta>0$,

$$\rho(r)=\begin{cases}\tfrac12r^2&|r|\le\delta\\\delta(|r|-\tfrac12\delta)&|r|>\delta\end{cases},\quad E=\sum_n w_n\rho(r_n),\quad\frac{\partial E}{\partial I_{j,n}}=w_n\operatorname{clip}(r_n,-\delta,\delta).$$

The exposure ratio is dimensionless; residuals retain intensity units and energy has squared intensity units. The derivative is continuous at the Huber boundary. Only aligned, calibrated samples are handled here.

## Visual computation trace

| Stage | Source 0.2, target 0.4 |
| --- | --- |
| Exposure ratio | 0.02 / 0.01 = 2 |
| Predicted target brightness | 2*0.2 = 0.4 |
| Corrected residual | 0.4-0.4 = 0 |
| Robust energy | 0 |

## Worked examples

1. Source `[0.2]`, target `[0.4]`, exposures `[0.01,0.02]`, zero log gains/offsets, weight `[1.]`, delta `0.1` yield residual `[0.]`, energy `[0.]`, target gradient `[0.]`, total `0`.
2. Source `[0.]`, target `[0.5]`, equal exposures, zero gains/offsets, weight `[0.5]`, delta `0.1` yield residual `[0.5]`, energy `[0.0225]`, target gradient `[0.05]`, total `0.0225`.

## Why this matters on a robot

Ignoring exposure can misinterpret an illumination change as camera motion. A robust loss reduces outlier influence but cannot fix an incorrect geometric warp or uncalibrated image response.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1607.02565). [warp-calibrated-pixels](/problems/warp-calibrated-pixels)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
