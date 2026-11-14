# Select Compact Visual Tokens with Learned Attention

Draft for review; this is not a published or runnable problem.

## Task

Compress a visual feature map into a small set of tokens. Each supplied logit map describes where one output token should look; normalize it over valid spatial positions and aggregate the original features.

$$
w_{bkn}=\frac{\exp(\ell_{bkn}-m_{bk})}{\sum_{j:V_{bj}=1}\exp(\ell_{bkj}-m_{bk})},\qquad z_{bkc}=\sum_nw_{bkn}F_{bnc},
$$

where $m_{bk}$ is the maximum valid logit. Invalid weights are exactly zero.

## Function

```python
def compact_visual_tokens(
    features: torch.Tensor,
    logits: torch.Tensor,
    valid: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    ...
```

## Inputs and outputs

- `features`: CPU float32 or float64 tensor `(B,N,C)`, with finite entries of magnitude at most `1e6`.
- `logits`: CPU tensor `(B,K,N)` with the same dtype; all entries finite and in `[-1e4,1e4]`, including masked positions.
- `valid`: `None` means every spatial position is valid; otherwise CPU bool tensor `(B,N)`. Every image must contain at least one valid position.
- Positive bounds: `B<=16`, `N<=4096`, `C<=256`, `K<=min(N,32)`; each input float tensor has at most `2_000_000` elements. Empty dimensions are unsupported.
- Return `(tokens, weights)` with shapes `(B,K,C)` and `(B,K,N)`, matching the float inputs’ dtype and device. Weights sum to one along `N`, up to numerical tolerance. No normalization over `K` or `C` is performed.
- Inputs may be noncontiguous. Do not mutate them or return outputs sharing their storage. Preserve autograd through features and logits, with zero influence from masked positions. No randomness or model parameters are created.

The features are dimensionless learned image descriptors. The caller flattens each image in row-major spatial order and supplies logits in the same order. This function neither moves a camera frame nor returns a robot action.

## Errors

Raise `TypeError` when a required argument is not a tensor, or `valid` is neither a tensor nor `None`. Raise `ValueError` for every tensor-contract violation: shape/bounds, dtype/device, nonfinite/out-of-range values, or an all-false valid row. Validate all entries, including masked padding; masking does not waive input validity.

Compute the normalization stably. A direct exponentiation of logits near `1e4` must not overflow. Time is `O(BKNC)`; the output and attention workspace are `O(BK(N+C))`.

## Worked examples

### Case1: two attention maps and one padded location

```text
features = [[[1,0], [3,2], [9,9]]]
logits = [[[0,ln(3),99], [0,0,99]]]
valid = [[True,True,False]]

tokens  = [[[2.5,1.5], [2,1]]]
weights = [[[0.25,0.75,0], [0.5,0.5,0]]]
```

Construct `ln(3)` in the chosen float dtype. The first token is `0.25*[1,0]+0.75*[3,2]`; the large masked logit contributes nothing. The second averages the two valid locations.

### Case2: independent single-location images

```text
features = [[[2]], [[-4]]]
logits = [[[1000]], [[-1000]]]
valid = None

tokens = [[[2]], [[-4]]]
weights = [[[1]], [[1]]]
```

Each batch item normalizes its own spatial axis. The large difference between images’ logits is irrelevant.

## Source and scope

This exercise isolates the spatial softmax and weighted aggregation in RT-1’s TokenLearner. Logits are supplied; learning their LayerNorm/MLP generator, image encoding, language conditioning, and policy training are out of scope. The optional padding mask is an original batching extension.

[Primary paper](https://arxiv.org/abs/2212.06817) · [Verified implementation reference](https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/tokenizers/token_learner.py#L103-L117).
