# Apply an Equivalent Channel Rescaling

## Intuition

Reduce a large activation channel by moving its scale into the matching weight row. The representation changes, while the linear function stays the same before rounding.

## Mathematics and conventions

Let $X\in\mathbb R^{N\times C}$, $W\in\mathbb R^{C\times D}$ and positive $s\in\mathbb R^C$. With $S=\operatorname{diag}(s)$,
$$\widetilde X=XS^{-1},\quad \widetilde W=SW,\quad\widetilde X\widetilde W=XW.$$
All features, scales and weights here are dimensionless. A possible calibration recipe is $s_j=a_j^\alpha/w_j^{1-\alpha}$, but zero guards and exponent choice belong to the caller. The required function consumes already validated positive scales. Floating-point equality is approximate; quantization later adds a different error source.

## Shape and numerical trace

```text
X(1,2)=[2,8] -> divide [2,4] -> [1,2]; W(2,1)=[3,4] -> multiply matching rows -> [6,16]; dot product 1*6+2*16=38.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Robot VLM calibration can move activation outliers without changing a layer in real arithmetic. Scaling weight columns instead of rows silently changes the function.

## Source and prerequisites

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
