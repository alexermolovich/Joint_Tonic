## Example 1

With B=H=F=C=L=1, history value 2, center kernel weight 3, head weight 4 and bias 1, the latent is 25 and used is true.

## Example 2

An all-false history returns latent 0 and used false even when the head bias is 1. A negative convolution value is clamped to zero before the head.
