# Choosing one explanation for an object

## Intuition

A detector may respond to one object several times. Greedy NMS chooses a strong candidate as an explanation and removes nearby same-class alternatives. It is deliberately asymmetric: the strongest surviving candidate determines what gets removed next.

## Suppression rule

Let $i$ be the highest-scoring remaining index and $j$ another remaining candidate. Remove j exactly when

$$
\operatorname{class}(j)=\operatorname{class}(i)
\quad\land\quad
\operatorname{IoU}(B_i,B_j)>\tau.
$$

Here $B_i$ is a continuous xyxy box in pixels and $\tau\in[0,1]$ is dimensionless. IoU is intersection area divided by union area; define it as zero for a zero union. Unlike a soft score update, hard NMS removes an index completely.

Order candidates by the pair $(-s_i,i)$, where $s_i$ is score. This specifies ties independently of machine or sorting implementation. The returned indices always refer to the original input, even after filtering the remaining candidates.

## Visual walkthrough

The NMS view highlights a selected box, displays its IoU against the remaining candidates, then labels each candidate “kept for next step,” “other class,” or “suppressed.” Single-step controls avoid dependence on animation. A table lists selected index, score, class, overlap, and reason.

## Worked chain example

Consider equal-height boxes A=`[0,0,2,2]`, B=`[1,0,3,2]`, C=`[2,0,4,2]`, scores `.9,.8,.7`, and threshold `.3`. A/B IoU is $2/(4+4-2)=1/3$, so A suppresses B. A/C IoU is 0, so C remains. The answer is `[A,C]`. Removing C merely because it overlaps B would be wrong: B was already suppressed and never becomes a selector.

## Class and threshold semantics

Two classes can legitimately describe different objects in the same location, so this exercise never suppresses across classes. At threshold 1, even identical boxes survive. At threshold 0, same-class boxes with any positive overlap suppress one another; merely touching boxes remain. These boundary choices are part of a deployment contract, not implementation trivia.

## Why this matters on a robot

Postprocessing affects how many obstacles or grasp targets the planner sees. Over-suppression can hide nearby objects; under-suppression can cause duplicate tracks. Benchmark the full inference graph, including NMS, and compare per-class/small-object slices. Preserve class order, box convention, threshold, and tie policy alongside the model version.

## Common failures

- Comparing every pair once can let discarded candidates remove valid boxes.
- Sorting each class separately and concatenating loses the global greedy order.
- Using `>=` at the IoU cutoff changes threshold-equality behavior.
- Forgetting original indices returns positions in a filtered list.

## Sources and scope

NMS is a common detector postprocessing tool and a companion to [YOLO v1](https://arxiv.org/abs/1506.02640). It is not the paper's novel contribution. This page, fixtures, and class-aware contract are original teaching material. See the prerequisite IoU problem for the continuous-rectangle geometry.
