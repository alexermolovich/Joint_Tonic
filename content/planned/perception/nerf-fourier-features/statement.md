# Encode 3D Positions with Fourier Features

Implement fourier_encode(positions, levels). positions is finite NumPy float64 (N,3), 0<=N<=10000, absolute coordinates<=1e4. Coordinates are dimensionless normalized scene coordinates in one fixed frame; normalization from meters is upstream. levels is a built-in int excluding bool in [0,10]. Return a new float64 array (N,6*levels). For each level ell=0..levels-1, append the three sin(2**ell*pi*positions) coordinates followed by the three cos coordinates; concatenate levels in increasing order. Do not prepend raw coordinates, mix coordinate-major order, or divide by pi. Preserve inputs and support noncontiguous arrays. levels=0 returns (N,0); N=0 returns (0,6*levels). TypeError for non-array positions, ValueError for all remaining violations. Values compared rtol=1e-7,atol=1e-9. No timestamps, neural network, random Fourier matrix, or view-direction encoding.

## Examples

## One frequency

positions=[[0,0.5,1]], levels=1. Output approximately [[0,1,0,1,0,-1]]. First three entries are sine, next three cosine.

## Two frequencies

positions=[[0.25,0,0]], levels=2. Let r=sqrt(2)/2. Output [[r,0,0,r,1,1,1,0,0,0,1,1]]. The second level uses 2*pi; tiny trigonometric rounding near zero is accepted.
