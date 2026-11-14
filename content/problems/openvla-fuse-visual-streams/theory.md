# Fuse Two Visual Feature Streams Safely

## Intuition

Two visual encoders can describe the same patch differently. Joining their feature channels gives a downstream projection access to both descriptions while preserving the patch sequence. Joining their token axes would instead pretend there were twice as many spatial positions.

## Feature-width fusion

Let $F^{(1)}\in\mathbb R^{B\times N\times C_1}$ and $F^{(2)}\in\mathbb R^{B\times N\times C_2}$ be aligned dimensionless patch features. B is batch size and N the common number of patches. Form

$$
U_{bn}=[F^{(1)}_{bn};F^{(2)}_{bn}]\in\mathbb R^{C_1+C_2}.
$$

For projection $W\in\mathbb R^{(C_1+C_2)\times E}$ and bias $c\in\mathbb R^E$, the unmasked output is $Z_{bn}=U_{bn}W+c$. E is the destination embedding width. Let $a_{bn},b_{bn}$ be the two Boolean validity inputs. Their intersection is $m_{bn}=a_{bn}\land b_{bn}$, and

$$
Y_{bn}=\begin{cases}Z_{bn},&m_{bn}=1,\\0,&m_{bn}=0.\end{cases}
$$

Mask after adding bias. Otherwise an invalid row can become a bias-only token that downstream attention interprets as observed evidence.

## Visual: a patch keeps one token position

| Stage | First patch | Second patch | Shape |
|---|---|---|---|
| First stream | [1,2] | [8,9] | 1 × 2 × 2 |
| Second stream | [3] | [4], invalid | 1 × 2 × 1 |
| Joined width | [1,2,3] | [8,9,4] | 1 × 2 × 3 |
| Projected and masked | [7.5,0] | [0,0] | 1 × 2 × 2 |

The table is an original static shape/value trace and text alternative. N stays two throughout. For the first row, [1,2,3] times the example projection is [1+6,2-3]=[7,-1], then bias gives [7.5,0].

## Gradients and alignment

For a scalar downstream objective L and an eligible row, the row gradient satisfies

$$
\frac{\partial L}{\partial U_{bn}}
=\frac{\partial L}{\partial Y_{bn}}W^\top.
$$

Split that feature gradient at C1 to recover the two streams' contributions. An invalid row contributes zero to features, W and c. The mask itself has no gradient.

Shape checks cannot prove geometric alignment: resized/cropped images can have the same patch count while covering different scene locations. The caller must preserve preprocessing, calibration and patch-order provenance.

## Why this matters on a robot

Complementary visual representations may help distinguish appearance from geometry, but mismatched patch locations combine evidence from different objects. An apparently valid fused tensor can therefore be physically misleading. This exercise tests the declared algebra and masks, not representation quality.

## Questions

Why preserve the token count? Each output still describes one aligned spatial patch. Why reject NaN even under a false mask? Input validation and validity masking have separate responsibilities.

Sources: [OpenVLA](https://arxiv.org/html/2406.09246v3) and its [feature concatenation implementation](https://github.com/openvla/openvla/blob/main/prismatic/models/backbones/vision/dinosiglip_vit.py). The affine projector and mask policy are bounded teaching choices. Prerequisite: [sensor projection](/problems/palm-e-project-sensor-features).
