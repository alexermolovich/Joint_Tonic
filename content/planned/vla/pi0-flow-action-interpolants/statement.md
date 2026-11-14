# Sample Flow-Matching Action Interpolants and Targets

Draft for review; this is not a published or runnable problem.

## Task

Construct a noised action chunk along a straight path from supplied noise at flow time0 to clean normalized actions at flow time1. Return the interpolant and the path’s velocity target.

## Function

```python
def flow_action_interpolants(
    actions: torch.Tensor,
    noise: torch.Tensor,
    tau: torch.Tensor,
    valid: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    ...
```

- `actions` and `noise` are CPU float32 or float64 tensors with identical shape `(B,H,D)` and dtype. All entries, including padding, must be finite and have magnitude at most `1e6`.
- `tau` is a CPU tensor `(B,)` with the same float dtype; every entry is finite and in `[0,1]`. Endpoints are supported.
- `valid` is a CPU bool tensor `(B,H)`. All-false masks are valid for this construction function and produce all-zero outputs.
- Bounds: `1<=B<=64`, `1<=H<=256`, `1<=D<=64`, and at most `2_000_000` scalars per action/noise input. Empty dimensions are unsupported.
- Before masking, compute `interpolant=(1-tau)*noise+tau*actions` with each tau reshaped to `(B,1,1)`. The target is `actions-noise`, independent of tau. Zero both returned tensors wherever valid is False.
- Both outputs have shape `(B,H,D)`, input float dtype/device, and independent storage not aliasing inputs or one another. Do not mutate inputs. Preserve autograd through actions, noise, and tau. Noncontiguous tensors are accepted.
- No random sampling, square-root coefficients, schedule cumulative product, model call, or normalization conversion is performed. The caller supplies already normalized Euclidean action channels.

## Errors and complexity

Raise `TypeError` if any argument is not a tensor. Raise `ValueError` for every tensor-contract violation: rank/shape/bounds, dtype/device, nonfinite/out-of-range values, or non-bool validity. A scalar tau is invalid even when B=1; this contract requires shape(B,).

Time and output memory are `O(BHD)`. This operation constructs generative training data; it sends no command to a simulator or robot.

## Worked examples

### Case1: fractional time across a two-step action chunk

```text
actions = [[[2,-2],[4,6]]]
noise = [[[0,2],[2,2]]]
tau = [0.25]
valid = [[True,True]]

interpolant = [[[0.5,1],[2.5,3]]]
target_velocity = [[[2,-4],[2,4]]]
```

For the last scalar,0.75*2+0.25*6=3 and its velocity target is6-2=4. The same flow time applies to every action coordinate in this batch item.

### Case2: different endpoints for different batch items

```text
actions = [[[2]], [[-1]]]
noise = [[[6]], [[3]]]
tau = [0,1]
valid = [[True],[True]]

interpolant = [[[6]], [[-1]]]
target_velocity = [[[-4]], [[-4]]]
```

The first item is exactly noise at tau0; the second is exactly clean action at tau1. The velocity target does not vanish at either endpoint.

## Source and scope

The task constructs training samples for the linear interpolation path described in pi0 SectionIV. Noise and flow times are supplied to make the exercise deterministic; it does not draw the paper’s timestep distribution, train a vector field, integrate an ODE, or reconstruct a full VLA. Padding masks are an explicit educational batching extension.

[Primary paper, arXiv2410.24164v4 SectionIV page5](https://arxiv.org/pdf/2410.24164v4). This pinned revision gives the actions-minus-noise velocity used here; earlier v1 printed the opposite sign.
