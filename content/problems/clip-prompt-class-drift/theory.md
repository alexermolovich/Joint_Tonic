# Detect Prompt and Class Distribution Drift

## Intuition

Prompt edits can move class directions even before camera data changes. Class histograms can shift even with unchanged prompts. Report both signals so one cannot hide the other.

## Math and diagnostic trace

For class $c$, old/new text vectors $a_c,b_c\in\mathbb R^D$ are normalized to unit vectors $\bar a_c,\bar b_c$. Their angular disagreement is $d_c=1-\bar a_c^\top\bar b_c$. For normalized old/new counts $p,q\in\mathbb R^C$ and midpoint $m=(p+q)/2$,
$$\operatorname{JS}(p,q)=\tfrac12\sum_{c:p_c>0}p_c\log(p_c/m_c)+\tfrac12\sum_{c:q_c>0}q_c\log(q_c/m_c).$$
All quantities are dimensionless. Natural-log JS ranges from0 to $\log2$; cosine distance ranges from0 to2. Missing mass in a class contributes zero for that distribution, avoiding log(0).

| Signal | Compared objects | Example |
|---|---|---|
| Prompt drift | normalized class vectors | orthogonal vectors → distance1 |
| Class drift | frequency proportions | disjoint one-hot histograms → ln2 |
| No drift | same directions/proportions | positive scale changes cancel |

For $p=(1,0),q=(0,1)$, midpoint is(0.5,0.5). Each nonzero KL contribution is ln2, so their average remains ln2.

## Why this matters on a robot

Renaming a target or changing camera scenes can alter which objects get selected. These statistics diagnose input changes without proving task degradation. Preserve class order and encoder identity; comparing different inventories under the same indices produces meaningless scores.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2103.00020). [clip-prompt-ensemble](/problems/clip-prompt-ensemble)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
