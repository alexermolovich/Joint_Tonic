# Apply a Weight-Pruning Mask

## Intuition

A pruning mask specifies which connections remain eligible for computation and later retraining. Keeping the mask separate from numerical zeros avoids confusing a retained zero with a deleted connection.

## Mathematics and conventions

For weights $W\in\mathbb R^{R\times C}$ and threshold $\tau\ge0$,
$$M_{ij}=\mathbf1[|W_{ij}|\ge\tau],\qquad \widetilde W_{ij}=M_{ij}W_{ij}.$$
$M$ is Boolean, $\widetilde W$ is float64, and both use the original row/column order. Absolute values treat positive and negative connections symmetrically. The exercise stops before the paper's retraining and entropy-coding stages.

## Shape and numerical trace

```text
[-.5,.2,0,1] -> magnitudes [.5,.2,0,1] -> threshold .5 -> [keep,drop,drop,keep] -> [-.5,0,0,1].
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Pruning can reduce the storage of robot perception networks. A sparse mask alone provides no hardware speedup guarantee; dropping negative weights by signed comparison changes the model incorrectly.

## Source and prerequisites

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
