# Balance a Multi-Dataset Training Mixture

## Intuition

A finite batch cannot realize every fractional dataset weight exactly. The rounding rule should be reproducible and visible. Largest-remainder allocation gives floor quotas first, then uses leftover items to cover the largest fractional deficits.

## Exact quotas and remainder allocation

For batch size B and nonnegative integer weights $w_i$ with $W=\sum_iw_i>0$, define

$$
q_i=\left\lfloor\frac{B w_i}{W}\right\rfloor,\qquad
r_i=(B w_i)\bmod W,\qquad
R=B-\sum_iq_i.
$$

All quantities are dimensionless counts or weights. Allocate $q_i+1$ to the R largest remainders, breaking ties by ID, and $q_i$ elsewhere. Integer arithmetic avoids rounding large weighted products through floats.

## Visual: a five-item batch

| Dataset | Weight | Ideal quota | Base | Remainder | Final |
|---|---:|---:|---:|---:|---:|
| disabled | 0 | 0 | 0 | 0 | 0 |
| large | 30 | 3.75 | 3 | 30 | 4 |
| small | 10 | 1.25 | 1 | 10 | 1 |

The bases use four items and the largest remainder receives the fifth. The table is the original visual and text alternative.

## A batch policy has limits

Every returned count is one of the two integers surrounding its ideal quota. Repeating identical small batches can repeatedly favor the same ID in remainder ties; this exercise does not implement rotation or stochastic fairness over training time. Sampling an episode versus a transition also changes a dataset's practical influence.

## Why this matters on a robot

Large datasets can dominate a naive loader, while rare embodiments need deliberate representation. A configured mixture makes that decision traceable, but count balancing does not align action semantics or ensure scenario diversity.

## Questions

1. Why can zero-weight sources still appear in the output?
2. Does this guarantee balanced exposure across repeated tiny batches?

## Sources and prerequisites

Open X-Embodiment motivates deliberate mixture composition. Hamilton largest-remainder allocation is an original deterministic batch-construction exercise, not a claim that RT-X uses this exact sampler. [Primary source](https://arxiv.org/abs/2310.08864), SectionIV training data mixture; exact apportionment is an original teaching choice. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

