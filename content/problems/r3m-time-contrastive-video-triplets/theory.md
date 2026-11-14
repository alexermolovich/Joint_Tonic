# Sample Time-Contrastive Video Triplets

## Intuition

Temporal supervision depends on which frames are compared. Choose an ordered anchor-near-far triple inside one video, then select a negative from a different video. Recorded draws let another engineer reproduce the same comparisons.

## Mathematical mechanism

Let $L_v$ be the frame count of video $v$, and let $u_0,\ldots,u_5\in[0,1)$ be one row of recorded draws. Choose $v$ from the sorted eligible IDs with $L_v\ge3$. Within that video, use $$i=\lfloor u_1(L_v-2)\rfloor,\quad j=i+1+\lfloor u_2(L_v-i-2)\rfloor,\quad k=j+1+\lfloor u_3(L_v-j-1)\rfloor.$$ Each remaining interval contains at least one frame, so $0\le i<j<k<L_v$. Draw the other video from all IDs except $v$, then its frame from $[0,L_{other})$. The output shapes are $(B,)$ for video IDs and negative frames, and $(B,3)$ for ordered frames. This conditional recipe is deliberately not uniform over all combinatorial triples; changing it changes the training distribution.

## Visual computation trace

| Draw stage | Available choices for lengths [3,2] | Zero draw result |
|---|---|---|
| Anchor video | [0] | 0 |
| Ordered frames | i=0, then j=1, then k=2 | [0,1,2] |
| Other video and frame | video1; frames [0,1] | (1,0) |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

lengths [3,2], uniforms [[0,0,0,0,0,0]] -> video_ids [0], frames [[0,1,2]], negative_video_ids [1], negative_frames [0].

## Why this matters on a robot

A negative from the same video can contradict the intended cross-video comparison. Reversing near and far frames changes the temporal objective. Uniform draws do not make every sequentially generated triple equally likely.

## Physical contract and limits

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

Source: [primary paper](https://arxiv.org/html/2203.12601v3). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
