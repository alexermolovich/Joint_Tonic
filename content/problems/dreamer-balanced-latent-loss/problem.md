# Compute a Balanced Latent-Model Loss

The dynamics prior should learn to predict the posterior, while the posterior should become easier to predict without discarding useful information. Separate gradient paths and a free-nat floor control this tradeoff.

## Contract

```python
def balanced_latent_loss(posterior_logits, prior_logits, prediction_loss, valid):
    ...
```

posterior_logits and prior_logits real (B,G,C), 1<=B<=128, 1<=G<=32, 2<=C<=32, abs<=50; prediction_loss real (B,) in [0,1e6], valid Boolean (B,). Each group is an independent categorical latent variable. Compute softmax s_q,s_p, then q=.99*s_q+.01/C, p=.99*s_p+.01/C. Per row K=sum over G,C q*(log(q)-log(p)), in nats. Dynamics loss max(1,KL(stop(q)||p)); representation loss max(1,KL(q||stop(p))); their forward values equal max(1,K), but gradient paths differ. Return dict kl float64(B) K valid else NaN; loss Python float mean over valid rows of prediction_loss+1.1*max(1,K) (0 if none); prior_gradient and posterior_gradient float64(B,G,C) analytical gradients with respect to input logits, using coefficient 1 on dynamics prior path and coefficient 0.1 on representation posterior path; prediction_gradient float64(B) 1/N valid else 0. At K<=1 both KL gradients exactly0 (explicit kink convention). Invalid rows have zero gradients and do not enter normalization. Include derivative of .99 softmax+.01/C. This implements the paper's specified loss balancing/free-nat/uniform-mixture component with supplied prediction losses, not the complete recurrent world model or straight-through latent sampling.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Example 1

Both categorical logits [0,0], one group, prediction_loss 2, valid True -> K=0, loss=3.1, both logit gradients 0,prediction_gradient 1.

## Example 2

Same inputs with valid False -> loss 0, kl NaN,all gradients 0. With two valid identical rows predictions [2,4],loss 4.1 and prediction_gradient [.5,.5].
