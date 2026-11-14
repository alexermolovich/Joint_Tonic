# Stable Softmax for Masked Sequences

Implement stable_masked_softmax(logits, valid) -> np.ndarray.

logits is NumPy float64(B,L), valid bool(B,L),1<=B<=256,0<=L<=2048,total<=200000. Every logit, including masked positions, is finite with magnitude<=10000. Return fresh float64(B,L). For each row with any valid entry, compute softmax over valid positions only using max subtraction; masked entries are exactly0. A row with no valid entries returns all zeros, without NaN; L=0 returns shape(B,0). Preserve inputs; noncontiguous arrays valid. Invalid contracts raise ValueError.

Logits are dimensionless relative evidence scores for a caller-ordered sensor/action token sequence. Mask presence is explicit; this function does not create a causal mask or enforce actuator constraints. Exact normalization is subject to standard float64 rounding.

## Worked examples

### Large equal valid logits
logits[[1000,1000,-1000]], valid[[True,True,False]] returns[[0.5,0.5,0]].

### Missing versus one available token
logits[[1,2],[5,9]], valid[[False,False],[True,False]] returns[[0,0],[1,0]].

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
