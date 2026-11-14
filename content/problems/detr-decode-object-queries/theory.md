# Decode Normalized Boxes and Classes from Object Queries

## Intuition

A DETR query is a prediction slot, not a guaranteed object. Its background score must compete with foreground classes. Decode the strongest foreground class first, then apply the supplied confidence threshold and padding mask; this exercise does not run matching or duplicate suppression.

## Mathematics and physical meaning

For one slot, $z\in\mathbb R^{C+1}$ contains dimensionless logits; index $C$ is the no-object class. With $m=\max_j z_j$, compute
$$p_j=\frac{\exp(z_j-m)}{\sum_{k=0}^{C}\exp(z_k-m)},\qquad \ell=\underset{0\le j<C}{\operatorname{argmax}}\ p_j.$$
Choose the smallest foreground index on ties. The returned score is $p_\ell$, not a renormalized foreground probability. With threshold $\tau$, validity is $v=\neg\mathrm{padding}\land(p_\ell\ge\tau)$. This still permits a foreground candidate when background is the overall maximum and the threshold is low.

A normalized box $(c_x,c_y,w,h)$ becomes
$$b=(c_x-w/2,\ c_y-h/2,\ c_x+w/2,\ c_y+h/2).$$
Clip each endpoint to $[0,1]$. Coordinates use the same image extent, with $x$ right and $y$ down; these are not metric robot coordinates. Inputs have shapes $(B,Q,C+1)$ and $(B,Q,4)$ for batch size $B$ and query count $Q$. Invalid slots return zero box/score and label $-1$.

## Visual trace

| Stage | One query |
|---|---|
| Foreground/background logits | `[0, 0]` |
| Full softmax | `[0.5, 0.5]` |
| Foreground score | `0.5` |
| Threshold 0.5, no padding | keep |
| Center box `[.5,.5,1,1]` | corners `[0,0,1,1]` |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** One query has logits `[0, 0]` (foreground, background), box `[.5,.5, 1, 1]`, no padding and threshold `.5`. Output: box `[0, 0, 1, 1]`, score `.5`, label `0`, valid `True`.

**Example 2.** Use the same input with threshold `.6`. Output: box `[0, 0, 0, 0]`, score `0`, label `-1`, valid `False`.

## Why this matters on a robot

A grasping pipeline needs to distinguish a candidate from an empty query. Dropping the background logit makes uncertain predictions look certain. A decoded 2D box alone supplies neither object depth nor a collision-free grasp.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2005.12872). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
