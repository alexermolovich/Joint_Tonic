# Encode Positive and Negative Point Prompts

Implement `encode_points(points: np.ndarray, labels: np.ndarray, image_size: tuple[int,int], frequencies: np.ndarray, type_embeddings: np.ndarray) -> np.ndarray`.

Encode supplied positive/negative point coordinates with random Fourier features and learned-type vectors.
points is float64 (N,2) with (x,y) pixel-index coordinates,0<=N<=4096; labels int64 (N,) is 0 negative or 1 positive. image_size is Python tuple (height,width), built-in positive ints<=100000. Require 0<=x<=width-1,0<=y<=height-1. frequencies is float64 (2,F),1<=F<=128,absolute values<=100; type_embeddings float64 (2,2F),row0 negative,row1 positive. Add 0.5 to each coordinate, divide by [width,height], map to [-1,1], multiply by frequencies and 2π. Return float64 (N,2F), concatenating ALL sine channels then ALL cosine channels, plus the corresponding type embedding. Frequencies and learned embeddings are supplied; do not sample random values. No padding label, resize, image encoder, or mask decoder is included.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. For image (1,1), point `[0,0]`, F=1, frequencies=`[[1],[0]]`, negative embedding `[0,0]` and positive embedding `[2,3]`: negative encodes `[0,1]`, positive `[2,4]`.
2. For image (2,2), point `[0,0]`, frequencies=`[[0.5],[0]]` and zero type vectors, normalized x=-0.5 and phase=-π/2; output `[-1,0]` (up to roundoff).

## Source and scope

[Primary source](https://arxiv.org/abs/2304.02643). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
