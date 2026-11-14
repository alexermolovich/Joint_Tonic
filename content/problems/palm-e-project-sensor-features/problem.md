# Project Continuous Sensor Features into Language Width

Implement project_sensor_features(features, weight, bias, valid), returning one fresh tensor (B,N,E).

features is a CPU float32/float64 tensor (B,N,C), weight (C,E), bias (E,), and valid a CPU bool tensor (B,N). All floating tensors share dtype and have finite entries with abs(value)<=1000. Require 1<=B<=32,0<=N<=1024,1<=C,E<=512; each floating input and output has <=2,000,000 elements. Empty N and all-false masks are valid. Inputs may be noncontiguous.

For valid tokens compute output[b,n,e]=sum_c features[b,n,c]*weight[c,e]+bias[e]. Invalid token rows are exactly zero, including the bias contribution. The bias is applied after the matrix product and masked afterward. Return matching dtype/device, no input mutation or storage alias, and preserve autograd through features, weight and bias. Masked rows have zero influence on every gradient. Do not create trainable parameters, normalize features, add positions, or merge batch/token axes semantically.

Raise TypeError if any argument is not a tensor. Raise ValueError for every tensor-contract violation, including invalid values in masked rows. Features are dimensionless normalized sensor descriptors measured in one synchronized observation per batch item. Row order stays unchanged; projected channels are language-embedding coordinates, not metric robot axes.

## Source and scope

Isolate a supplied affine projection into a language embedding width. PaLM-E permits richer modality encoders; this exercise does not assert every encoder is one affine layer. Inputs are already normalized modality features, not raw heterogeneous physical units.

[Primary paper](https://arxiv.org/abs/2303.03378).


## Worked examples

### Two sensor tokens and a bias

features=[[[1,2],[3,4]]], weight=[[1,0,-1],[0,2,1]], bias=[0.5,-1,2], valid=[[True,True]].

Return [[[1.5,3,3],[3.5,7,3]]]. The first matrix product is [1,4,1]; adding the bias gives [1.5,3,3].

### A missing token must not receive bias

features=[[[2],[-5]]], weight=[[3,4]], bias=[1,-1], valid=[[True,False]].

Return [[[7,7],[0,0]]]. Multiplying a masked feature by zero before adding bias would incorrectly produce [1,-1] in the invalid row.


## Hints

1. Matrix multiplication can preserve the B and N axes automatically.
2. Broadcast bias over the leading axes.
3. Expand valid with one trailing axis and apply it after adding bias.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4, PyTorch 2.6.0 CPU. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=1e-6 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
