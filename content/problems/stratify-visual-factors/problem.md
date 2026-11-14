# Stratify Texture, Lighting, Camera, and Distractor Factors

Implement stratify_visual_factors(permutations, jitter) -> np.ndarray.

permutations is a NumPy int64(N,4) array,1<=N<=10000. Every column must independently be a permutation of0..N-1. jitter is a matching NumPy float64 array, finite in[0,1). Noncontiguous arrays are valid. Return new float64(N,4) values(permutations+jitter)/N. Column meanings are normalized texture-choice coordinate, lighting coordinate, camera coordinate, and distractor-choice coordinate.  Floating-point boundary policy: clamp the computed value to at least lower=permutations/N and at most np.nextafter(upper,lower), where upper=(permutations+1)/N, so rounding cannot cross a half-open stratum boundary. Each factor occupies every one of N half-open strata exactly once; rows define joint scenarios. Preserve inputs and avoid storage aliasing. All invalid types/dtypes/shapes/permutations/values raise ValueError.

The caller supplies permutations and jitter; no RNG occurs. These are dimensionless design coordinates, not actual texture IDs, light intensities or camera poses. Categorical mapping and physical bounds belong downstream. This Latin-hypercube-style marginal design does not promise coverage of all N^4 joint cells or reproduce a paper's exact sampler.

## Worked examples

### Two complementary rows
For permutations[[0,1,0,1],[1,0,1,0]] int64 and jitter filled with0.5 float64, return[[0.25,0.75,0.25,0.75],[0.75,0.25,0.75,0.25]].

### One scenario
For permutations zeros(1,4) int64 and jitter[[0,0.2,0.5,0.9]] float64, return that jitter row unchanged in new storage.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
