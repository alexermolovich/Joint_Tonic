# Give sensor features the language model's width

## Intuition

A language model expects a fixed number of coordinates per token. A sensor encoder may emit a different width. A learned projection aligns that width so sensor descriptors can occupy token positions beside text. Matching width alone does not make the coordinates semantically meaningful; training learns the alignment.

## An affine map shared by tokens

Let $F\in\mathbb R^{B\times N\times C}$ be normalized sensor features, $W\in\mathbb R^{C\times E}$ the supplied projection and $\mathbf b\in\mathbb R^E$ its bias. $B$ is batch size, $N$ sensor-token count, $C$ sensor-feature width and $E$ language width. For validity mask $V\in\{0,1\}^{B\times N}$,

$$
Y_{bne}=V_{bn}\left(\sum_{c=0}^{C-1}F_{bnc}W_{ce}+b_e\right).
$$

All these coordinates are dimensionless learned features. A metric pose or timestamp must be normalized and encoded upstream under a declared physical contract. The same W and bias apply to every token without mixing examples or token positions.

## Visual: width changes, positions remain

| Stage | Shape | What changes |
|---|---|---|
| Sensor features | B × N × C | Normalized encoder output |
| Multiply by W | B × N × E | Feature width C becomes E |
| Add bias | B × N × E | Same E-vector at each token |
| Apply validity | B × N × E | Invalid rows become zero |

This static shape trace is also its text alternative. The token axis N survives unchanged.

For feature [1,2] and weight rows [1,0,-1] and [0,2,1], the matrix product is [1,4,1]. Adding bias [0.5,-1,2] gives [1.5,3,3]. A false validity entry replaces the entire result with [0,0,0].

## Gradients and masking

If $G$ is the upstream output gradient, an invalid token has $V_{bn}=0$ and contributes nothing to feature, weight, or bias gradients. Masking only before the bias would violate this rule. The projection stays differentiable so an end-to-end model can improve its modality alignment.

## Why this matters on a robot

A missing wrist-camera observation should not turn into an ordinary bias-only visual token. Stale or poorly normalized sensor inputs can look numerically plausible after projection, so validate freshness and calibration before this layer. An all-zero embedding alone is not a complete attention mask; carry validity to the downstream transformer too.

## Check your understanding

1. Does projection combine adjacent camera tokens? No; it mixes feature channels within each token.
2. Why mask after adding bias? Missing rows must remain zero and contribute no bias gradient.
3. Can an embedding be sent directly to a joint controller? No; it has no actuator units or frame.


## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.03378), Sections3–4: continuous sensor embeddings. Isolate a supplied affine projection into a language embedding width. PaLM-E permits richer modality encoders; this exercise does not assert every encoder is one affine layer. Inputs are already normalized modality features, not raw heterogeneous physical units.

Prerequisites: the stated robotics data contract and tensor axes; no general Python or mathematics lesson.


## Numerical shape trace

| Input | Projection | Masked output |
|---|---|---|
| B × N × C | C × E, then E bias | B × N × E |
| Valid row [2] | [3,4], bias [1,-1] | [7,7] |
| Invalid row [-5] | Same projection | [0,0] |
