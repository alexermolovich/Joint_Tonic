# Compute a Masked CVAE Reconstruction and KL Loss

Implement cvae_loss(prediction, target, valid, mean, log_variance, beta), returning a tuple (total, reconstruction, kl) of fresh zero-dimensional tensors.

prediction and target are finite CPU float32/float64 tensors of identical shape (B,H,D), dtype, and absolute value <=1e6. valid is a CPU bool tensor (B,H) with at least one True globally; individual items may contain no valid actions. mean and log_variance are CPU tensors of matching floating dtype and identical shape (B,Z), with finite values: abs(mean)<=1000 and -20<=log_variance<=20. All dimensions are positive; B<=64,H<=256,D<=64,Z<=256; each floating tensor has <=2,000,000 elements. beta is a built-in non-bool int/float, finite and in [0,100].

Reconstruction is the sum of absolute prediction-target residuals at valid timesteps, divided by D*valid.sum(). KL is 0.5 times the batch mean of the latent-dimension sum mean**2+exp(log_variance)-1-log_variance. Include every batch item's KL even if its action mask is empty. total=reconstruction+beta*kl. log_variance is log(sigma**2), not log(sigma).

Keep dtype/device and autograd through all four floating tensors; do not detach target or return Python numbers. At an exact zero residual, use the standard absolute-value subgradient zero. Accept noncontiguous tensors; preserve inputs. Validate masked padding too. All-false global validity is an error even if beta>0.

Raise TypeError for non-tensor tensor arguments or non-built-in numeric beta. Raise ValueError for every shape/dtype/device/bounds/finiteness violation. Errors are normalized Euclidean action coordinates, with fixed horizon control interval chosen upstream; latent dimensions have no robot frame or physical units. No circular/quaternion reconstruction or safety guarantee.

## Source and scope

Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The global valid-scalar reconstruction mean and batch-mean latent sum are explicit teaching reductions. No encoder, latent sampling, transformer, or training run is reproduced.

[Primary paper](https://arxiv.org/abs/2304.13705).


## Worked examples

### Reconstruction and a nonzero latent penalty

prediction=[[[1,3],[100,100]]], target=[[[0,1],[0,0]]], valid=[[True,False]], mean=[[1,0]], log_variance=[[0,0]], beta=2.

The valid absolute residuals are 1 and 2, so reconstruction=1.5. Unit variance with mean [1,0] gives KL=0.5. Return (2.5,1.5,0.5), as scalar tensors.

### Variance is exponentiated, not squared

prediction=[[[0]],[[2]]], target=zeros, valid=[[True],[True]], mean=[[0],[0]], log_variance=[[ln(4)],[0]], beta=1.

Reconstruction=1. KL=(3-ln(4))/4, approximately0.4034264097. Total is approximately1.4034264097. The first variance is4; the second posterior equals the standard normal prior.


## Hints

1. Broadcast the timestep mask over action channels.
2. Compute variance with exp(log_variance), not exp(2*log_variance).
3. Sum latent dimensions and average batch items; reconstruction uses a different denominator.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4, PyTorch 2.6.0 CPU. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=1e-6 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
