# Combine Temporal and Language Alignment Losses

Nearby visual states, meaningful language progress and compact features provide different learning signals. Compute each term explicitly before combining them, so a large regularizer cannot hide a reversed contrastive target.

## Contract

Embeddings real (B,4,D), 0<=B<=512, 1<=D<=256, absolute values<=100. Slots are anchor i, nearby j, farther k, and other-video anchor; ordering and video identity have already been validated. Language logits real(B,3), absolute values<=1000, ordered positive later/correct-language, earlier/correct-language, other-video/correct-language. These are supplied scores from a learned progress model, not image-caption cosine similarities. Valid bool(B,), weights real(4,) in[0,100]. Compute temporal logits [-norm(zi-zj), -norm(zi-zk), -norm(zi-zother)] using Euclidean norm, then negative log-softmax at index0. Language term is negative log-softmax(language_logits) at index0. L1 and L2 terms are respectively sum(abs(zi)) and sqrt(sum(zi**2)) for anchor embedding, NOT squared L2. Return dict per_example float64(B,4) (invalid rows zero), components float64(4,) (mean over valid rows, or zeros when none), loss Python float dot(weights,components). Averaging convention and anchor-only regularization are explicitly pinned; the paper's batch-summed objective differs only in the declared reduction/weight scale. No gradients or model training requested. Every input including invalid rows is still validated.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Example 1

B=D=1, all four embeddings zero, language logits [0,0,0], valid True, weights [1,1,1,1]: components [log(3),log(3),0,0], loss 2log(3).

## Example 2

all four embeddings [3,4], all language logits zero, weights [0,0,2,3], valid True: components [log(3),log(3),7,5], loss29. With valid False, per_example and all outputs are zero.
