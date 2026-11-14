# Update Occupancy Belief from Range Evidence: theory

## Intuition

One range reading should influence a map cell without making it permanently certain. Occupancy mapping stores a belief that a cell contains an obstacle. Repeated obstacle observations strengthen it; observations of free space weaken it. Log odds turn this evidence accumulation into addition, which is convenient for incremental maps.

## What the stored value means

For occupancy probability $p\in(0,1)$, define

$$
L(p)=\log\frac{p}{1-p},\qquad
p(L)=\frac{1}{1+e^{-L}}.
$$

Both quantities are dimensionless. Zero log odds means equal occupied/free probability. Positive values favor occupied; negative values favor free. The grid's cell size and map frame determine physical geometry, but they do not change the probability formula.

Let $L_t$ be the current belief, $p_{\mathrm{inv}}$ the inverse sensor model's probability for the latest observation, and $p_0$ the prior assumed by that model. The update is

$$
L_{t+1}=\operatorname{clip}\left(
L_t+L(p_{\mathrm{inv}})-L(p_0),L_{\min},L_{\max}
\right).
$$

Subtracting the prior avoids adding the model's initial assumption every time. When the sensor model uses a 0.5 prior, that correction is zero. It must still be part of the contract because other priors produce different evidence.

## Worked range example

Begin with $p=0.5$, so $L=0$. A hit whose inverse-model probability is 0.8 contributes $\log4$. The new belief is 0.8. A second identical hit contributes another $\log4$, producing $\log16$ and probability $16/17$, approximately 0.941176. These are two observations of the same cell, not two obstacle objects.

A free-space observation with inverse-model probability 0.2 contributes $-\log4$. Starting at probability 0.8, that equal-strength opposite evidence returns the belief to 0.5 before clamping.

## Visual explanation

Display a cell with hit/free observation buttons, a belief bar, and a log-odds history. A table shows prior correction, evidence increment, unclamped value, and final probability. Label unobserved cells explicitly instead of coloring them as free.

## Robot relevance and failure modes

A planner may regard unknown space differently from known free space. Confusing them creates unsafe routes. Clamping avoids numerical certainty that later observations cannot overturn, but bounds are policy choices. Correlated repeated scans, pose error, and moving objects can invalidate this simple evidence model. The lesson teaches occupancy as a probabilistic representation before comparing it with learned spatial representations such as BEV features; it does not claim those representations use this update.

