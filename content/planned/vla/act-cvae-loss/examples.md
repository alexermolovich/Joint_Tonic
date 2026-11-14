# Worked examples

## Reconstruction and a nonzero latent penalty

prediction=[[[1,3],[100,100]]], target=[[[0,1],[0,0]]], valid=[[True,False]], mean=[[1,0]], log_variance=[[0,0]], beta=2.

The valid absolute residuals are 1 and 2, so reconstruction=1.5. Unit variance with mean [1,0] gives KL=0.5. Return (2.5,1.5,0.5), as scalar tensors.

## Variance is exponentiated, not squared

prediction=[[[0]],[[2]]], target=zeros, valid=[[True],[True]], mean=[[0],[0]], log_variance=[[ln(4)],[0]], beta=1.

Reconstruction=1. KL=(3-ln(4))/4, approximately0.4034264097. Total is approximately1.4034264097. The first variance is4; the second posterior equals the standard normal prior.
