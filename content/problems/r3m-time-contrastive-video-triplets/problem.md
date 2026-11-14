# Sample Time-Contrastive Video Triplets

Temporal supervision depends on which frames are compared. Choose an ordered anchor-near-far triple inside one video, then select a negative from a different video. Recorded draws let another engineer reproduce the same comparisons.

## Contract

Lengths integer (V,), 2<=V<=1024, each 1..100000; implicit video IDs are row indices. At least one video has length >=3. Uniforms real (B,6), 0<=B<=16384, every entry in [0,1). At each batch row: draw the anchor video uniformly from the sorted IDs with length>=3 using column 0; draw i=floor(u1*(L-2)); j=i+1+floor(u2*(L-i-2)); k=j+1+floor(u3*(L-j-1)); draw a different video from sorted remaining IDs with column 4; draw its frame floor(u5*other_length). Return dict video_ids int64(B,), frames int64(B,3), negative_video_ids int64(B,), negative_frames int64(B,). Output obeys i<j<k and negative video != anchor video. Frame indices are zero-based ordinal positions; no constant frame-rate or seconds implied. This is an explicit replayable sequential sampling recipe, NOT a uniform distribution over all possible triples or a claim to match the paper's random sampler exactly.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Example 1

lengths [3,2], uniforms [[0,0,0,0,0,0]] -> video_ids [0], frames [[0,1,2]], negative_video_ids [1], negative_frames [0].

## Example 2

lengths [5,3,4], uniforms [[0.5,0.9,0.9,0.9,0.9,0.9]] -> anchor video 1, frames [[0,1,2]], negative video 2, negative frame 3. Empty B returns four correctly shaped empty arrays.
