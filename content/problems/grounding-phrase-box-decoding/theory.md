# Decode Phrase-Labeled Boxes

## Intuition

Detector outputs live in two different coordinate systems: normalized image boxes and token-level language scores. Decoding must preserve both query identity and phrase identity while converting geometry to pixels.

## Math and output trace

For query $q$, token $t$ has logit $\ell_{qt}$. Phrase $p$ owns token set $J_p$, so this teaching decoder uses
$$s_{qp}=\max_{t\in J_p}\sigma(\ell_{qt}),\qquad p_q=\arg\max_p(s_{qp},-p).$$
The tie notation means choose the smallest phrase index. Keep query $q$ when $s_{q,p_q}\ge\tau$. For normalized center-size box $(c_x,c_y,w,h)$ and image size $(H,W)$,
$$b_{xyxy}=(W(c_x-w/2),H(c_y-h/2),W(c_x+w/2),H(c_y+h/2)).$$
Scores are dimensionless; decoded corners are pixels with x right,y down. Normalized center coordinates can be valid while corners extend outside the image.

| Stage | Shape | Identity retained |
|---|---|---|
| Token logits | Q × T | query/token |
| Phrase aggregation | Q × P | query/phrase |
| Best phrase and threshold | K | original query index |
| Pixel conversion | K × 4 | geometry of that same query |

At zero logits all token probabilities are 0.5, so phrase0 wins a tie and threshold0.5 passes. The example width is 0.5×200=100 pixels centered at100, giving horizontal corners50 and150.

## Why this matters on a robot

Dropping original indices can attach a selected mask to the wrong box. Clipping boxes silently changes geometry used by a later prompt encoder. This max-token phrase rule is explicitly chosen for the exercise, not a universal calibration rule for Grounding DINO outputs.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). [grounding-token-phrase-map](/problems/grounding-token-phrase-map)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
