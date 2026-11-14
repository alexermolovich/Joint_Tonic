# Compute Group-Wise Quantization Parameters

## Intuition

Small groups share one scale and zero point so each group can use its available integer levels efficiently. Group boundaries and rounding order are part of the serialized model contract.

## Mathematics and conventions

A row is split into $G=C/g$ contiguous groups of $g$ weights. Let $l=\min(0,\min w)$, $h=\max(0,\max w)$ and $Q=2^b-1$ for bit count $b$.
$$s=\max((h-l)/Q,\operatorname{tiny}_{64}),\quad z=\operatorname{clip}(\operatorname{rint}(-l/s),0,Q),\quad q=\operatorname{clip}(\operatorname{rint}(w/s)+z,0,Q).$$
Here $\operatorname{tiny}_{64}=2^{-1022}$ is the smallest positive normal float64 value; the floor preserves a nonzero divisor even for subnormal ranges. For an all-zero group define $s=1,z=0$. Reconstruct $\widehat w=(q-z)s$. The uint8 container stores logical $b$-bit values; bit packing is out of scope. All values are dimensionless and rounding is ties-to-even. Including zero avoids a special nonzero-constant-group encoding but is an explicit teaching choice.

## Shape and numerical trace

```text
W(1,4) -> groups(1,2,2):[-1,1]|[0,3] -> scales[2/3,1], zeros[2,0] -> q[0,3]|[0,3] -> reconstructed[-4/3,2/3]|[0,3].
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Packing with a different grouping or zero-point convention than serving expects corrupts a robot model even when shapes match. Validate numerical layer error before making memory or task-quality claims.

## Source and prerequisites

Original bounded component inspired by [2023-awq](https://arxiv.org/abs/2306.00978). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
