# Sample an Action Trajectory with DDPM Steps

Reverse diffusion removes predicted corruption one level at a time. The variance of each injected random term must match the selected reverse schedule, and the final step must not add fresh noise.

## Contract

`sample_ddpm_actions(initial,predicted_noise,betas,step_noise)` receives initial(H,D),1<=H,D<=64; predicted_noise and step_noise:(K,H,D),1<=K<=64, abs all three tensors<=100; betas(K,) each in [0.0001,0.1]. Arrays at index k correspond to forward diffusion level k+1. Return float64 trajectory(K+1,H,D): first initial noisy sample, then states after reverse levels K,...,1. Let alpha=1-beta, abar=cumprod(alpha), previous_abar=1 at k=0 else abar[k-1], posterior_var=beta[k]*(1-previous_abar)/(1-abar[k]). At reverse index k compute mean=(x-beta[k]/sqrt(1-abar[k])*predicted_noise[k])/sqrt(alpha[k]); next=mean+sqrt(posterior_var)*step_noise[k] for k>0; at k=0 return mean without noise. Supplied predictions represent already evaluated denoiser outputs, not a callable model. No clipping or extra random draw.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions are normalized dimensionless controller channels; diffusion coefficients and noise are dimensionless. Diffusion indices are noise levels, not robot control timestamps; each H row denotes a future action slot. Original DDPM posterior-variance teaching sampler motivated by Diffusion Policy. A real policy recomputes its conditional denoiser on each current state; this task supplies those outputs to isolate scheduler arithmetic.


## Example 1

initial=[[1]], predicted_noise=[[[0]]], betas=[0.04], step_noise=[[[99]]] gives trace [[[1]],[[1/sqrt(0.96)]]]. Final noise is ignored even though nonzero.

## Example 2

initial=[[0]], predicted_noise=zeros((2,1,1)), betas=[0.04,0.04], step_noise=[[[0]],[[1]]] gives states 0, sqrt(0.04*0.04/0.0784), then that value/sqrt(0.96). Noise enters only at reverse index1.
