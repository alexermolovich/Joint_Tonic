# Assemble a Pre-Norm Vision Transformer Block

Implement `vit_block(tokens: np.ndarray, parameters: dict) -> np.ndarray`.

Implement a single-head, dropout-free pre-norm transformer encoder block with supplied parameters.
tokens float64 (N,D),1<=N<=128,1<=D<=64, are dimensionless patch/class embeddings in fixed order. parameters is exactly a dict with float64 arrays: q,k,v,o (D,D), w1 (D,F),b1(F,),w2(F,D),b2(D,),gamma(2,D),beta(2,D),1<=F<=128. For each token, layer norm uses population variance and epsilon1e-5, then row-specific gamma/beta (row0 first norm,row1 second). Set z=LN0(tokens), attention=softmax((z@q)@(z@k).T/sqrt(D)) over keys, u=tokens+(attention@(z@v))@o. Return u+GELU(LN1(u)@w1+b1)@w2+b2, exact GELU(x)=0.5*x*(1+erf(x/sqrt2)). No qkv bias, attention mask, positional addition, final norm, dropout or multi-head split. All supplied values have absolute value<=100 (tighter than general rule). Return fresh float64(N,D).

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With q,k,v,o,w1,w2 and both biases all zero, gamma all ones and beta zeros, output equals tokens exactly: both residual branches contribute zero.
2. For one token `[2,4]`, zero attention branch and zero w1,w2, b2=`[1,-1]`, output is `[3,3]`. No final layer normalization is applied.

## Source and scope

[Primary source](https://arxiv.org/abs/2010.11929). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
