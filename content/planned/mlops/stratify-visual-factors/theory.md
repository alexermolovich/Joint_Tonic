# Stratify Texture, Lighting, Camera, and Distractor Factors

## Intuition

Pure random draws can leave gaps in individual factor ranges. Stratification forces each factor to visit every interval once, while supplied permutations avoid always pairing low values with low values.

## One visit per marginal stratum

For scenario i and factor j, $P_{ij}$ is an integer stratum index and $U_{ij}\in[0,1)$ is jitter. With N scenarios,

$$X_{ij}=\frac{P_{ij}+U_{ij}}N,\quad \left\lfloor NX_{ij}\right\rfloor=P_{ij}.$$

Each column of P is a permutation of0 through N-1. This controls one-dimensional marginals only. A full factorial grid would require N^4 combinations, which this N-row design does not provide.

## Visual: two scenarios, four factors

| Scenario | Texture | Light | Camera | Distractor |
|---|---:|---:|---:|---:|
| 0 | 0.25 | 0.75 | 0.25 | 0.75 |
| 1 | 0.75 | 0.25 | 0.75 | 0.25 |

With N2 and jitter0.5, each column visits its lower and upper half once. This original table is the design diagram and text alternative.

## Why this matters on a robot

Coverage across light and camera variation can reveal fragile perception. Mapping a normalized coordinate to categories may merge strata, so inspect actual rendered-condition coverage as well. Marginal balance alone can still miss a difficult joint combination.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.


## Floating-point boundary handling

 Floating-point boundary policy: clamp the computed value to at least lower=permutations/N and at most np.nextafter(upper,lower), where upper=(permutations+1)/N, so rounding cannot cross a half-open stratum boundary. This guard only changes rounded boundary values, preserving the declared stratification for jitter arbitrarily close to one.
