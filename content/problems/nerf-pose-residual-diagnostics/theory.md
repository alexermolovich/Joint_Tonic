# Detect Bad Poses with Reprojection and Render Residuals

## Intuition

A wrong pose often damages both where landmarks project and what a renderer predicts. Keeping those signals separate prevents a good color score from hiding a geometric error. Missing observations need their own status.

## Math and denominator choices

For view $v$, let $S_v$ be its valid sample indices and $n_v=|S_v|$. Pixel residual $e_{vi}\in\mathbb R^2$ has pixel units; RGB residual $r_{vi}\in[-1,1]^3$ is dimensionless linear color.
$$E_v=\sqrt{\frac1{n_v}\sum_{i\in S_v}\|e_{vi}\|_2^2},\qquad C_v=\sqrt{\frac1{3n_v}\sum_{i\in S_v}\|r_{vi}\|_2^2}.$$
The factor 3 averages color channels; there is no factor 2 for pixel error because the metric measures Euclidean image distance. For $n_v=0$ return explicit unobserved status and zero placeholders. A view is flagged only if observed and $E_v>\tau_p$ or $C_v>\tau_c$.

| Residual | Squared contribution | Reported metric |
|---|---|---|
| Pixel (3,4) | 9+16=25 | 5 pixels |
| RGB (1,0,0) | 1/3 | 1/√3 |
| No valid samples | no evidence | zero placeholder + observed=false |

## Why this matters on a robot

Specular reflections can raise color error without moving landmarks; a stale pose can shift both. These diagnostics support triage, not causal identification. Comparing across cameras requires equivalent calibration, masking and color preprocessing. The supplied residual analysis is an original teaching component rather than NeRF's full optimization loop.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2003.08934). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
