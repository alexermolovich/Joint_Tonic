# Evaluate Localization and Phrase Grounding Separately

## Intuition

A box can be geometrically correct while naming the wrong object, or name the right phrase while pointing elsewhere. Report these failures separately before combining them. The exercise receives matched pairs; it does not infer detection assignments or dataset precision.

## Mathematics and physical meaning

For pair $i$, predicted and target boxes use normalized $(x_1,y_1,x_2,y_2)$ with positive width/height in one image. Intersection-over-union is
$$u_i=\frac{|P_i\cap G_i|}{|P_i|+|G_i|-|P_i\cap G_i|}.$$
Areas use normalized image units squared. For validity $v_i$, shared-vocabulary phrase identifiers $a_i,b_i$, and threshold $\tau$, define
$$l_i=v_i\land(u_i\ge\tau),\quad p_i=v_i\land(a_i=b_i),\quad g_i=l_i\land p_i.$$
Each rate divides its true count by $n=\sum_i v_i$; all three rates are zero when $n=0$. Invalid rows have IoU zero and false flags. With arrays of $N$ paired examples, the output diagnostics remain shape $(N,)$. The threshold includes equality. This is a paired agreement diagnostic, not mAP, recall or calibration.

For extremely small positive boxes, compute area ratios after scaling both boxes by the same per-axis extent. This leaves IoU unchanged while avoiding an avoidable zero-over-zero from area underflow.

## Visual trace

| Pair | Localization | Phrase | Joint grounding |
|---|---|---|---|
| Same box, different phrase | pass | fail | fail |
| Disjoint boxes, same phrase (threshold .5) | fail | pass | fail |
| Same box and phrase | pass | pass | pass |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** An identical predicted/target box with different phrase IDs and threshold `.5` has IoU `1`, localization rate `1`, phrase rate `0`, and joint grounding rate `0`.

**Example 2.** Disjoint predicted/target boxes with the same phrase ID and threshold `.5` have localization rate `0`, phrase rate `1`, and joint grounding rate `0`.

## Why this matters on a robot

A manipulation failure may come from perception geometry or language interpretation. One combined score can hide which subsystem needs attention. Supplied pairs must already share the same image and vocabulary; index equality across incompatible vocabularies is meaningless.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
