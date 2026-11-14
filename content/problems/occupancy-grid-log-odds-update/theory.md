# Update Occupancy Grid Log Odds

## Intuition

Occupancy is a binary hypothesis. Converting probability into log odds turns repeated Bayesian evidence into addition; subtracting the prior prevents counting the same prior once per observation.

## Mathematics and physical meaning

For occupied probability $p\in(0,1)$, define $\operatorname{logit}(p)=\log p-\log(1-p)$. At grid cell $(r,c)$ the current log odds are $L_{rc}$. An inverse-sensor probability $p_k$ contributes evidence relative to prior $p_0$:
$$L_{rc}\leftarrow\operatorname{clip}\bigl(L_{rc}+\operatorname{logit}(p_k)-\operatorname{logit}(p_0),-b,b\bigr).$$
$b>0$ is the saturation limit, dimensionless like log odds. Convert back using $P(\mathrm{occupied})=1/(1+e^{-L})$. Clipping occurs after each observation, so evidence ordering can matter near saturation. The inverse sensor model itself is supplied, not estimated here.

## Visual trace

| Cell evidence, prior=0.5 | Log odds | Occupied probability |
|---|---|---|
| Start | 0 | 0.5 |
| Observe p=0.8 | log(4) | 0.8 |
| Observe p=0.8 again, limit=2 | 2 (clipped) | about 0.8808 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `log_odds=[[0]], observations=[[0,0,0.8],[0,0,0.8]], prior=0.5, limit=2` → `[[2.0]]`.
2. `log_odds=[[0.3,-0.2]], observations=[[0,1,0.7]], prior=0.7, limit=4` → `[[0.3,-0.2]]`; evidence equal to the prior is neutral.

## Why this matters on a robot

Clipping keeps a long-lived map from becoming infinitely certain, allowing later evidence to clear a cell. Treating correlated repeated scans as independent still makes the map overconfident. This exercise performs neither ray tracing nor collision checking.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
