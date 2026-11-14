# Constrain Autoregressive Decoding to Valid Actions

## Intuition

A model may prefer an ordinary language token even when the next field must be a robot action. Constrained decoding makes the output grammar explicit before normalizing or choosing a token. It cannot determine whether a valid action achieves the task.

## Restrict the support

Let $L\in\mathbb R^{B\times V}$ be finite dimensionless logits, $p_b$ the next field position for batch row $b$, and $\mathcal A$ the supplied set of action token IDs. There are $D$ action channels, represented by the channels argument. The allowed set is

$$
S_b=\begin{cases}\{0,1\},&p_b=0,\\\mathcal A,&1\le p_b\le D.\end{cases}
$$

Use the largest allowed logit $m_b=\max_{j\in S_b}L_{bj}$ for stable normalization:

$$
P_{bj}=\begin{cases}
\dfrac{\exp(L_{bj}-m_b)}{\sum_{k\in S_b}\exp(L_{bk}-m_b)},&j\in S_b,\\
0,&j\notin S_b.
\end{cases}
$$

Subtracting a shared maximum preserves probability ratios and avoids overflow. Masking probabilities after a full-vocabulary softmax would leave an incorrectly normalized row. Return the smallest ID among allowed maximizers:

$$
\hat\tau_b=\min\{j\in S_b:L_{bj}=m_b\}.
$$

## Visual: the same vocabulary has different legal fields

| Token ID | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Position 0: flag | allowed | allowed | blocked | blocked | blocked |
| Position 1 or 2: action | blocked | blocked | allowed | blocked | allowed |

This original table is the static mask diagram and text alternative for vocabulary [4,2]. In the first example the flag row normalizes weights 1 and 3 into 1/4 and 3/4; logit 50 is irrelevant because its fields are illegal. The second row makes the same calculation over action IDs 2 and 4.

## Autoregressive use and boundaries

In a full decoder, the selected token becomes part of the next model input and the field position advances. Here one step receives already computed logits. The fixed-width grammar deliberately still requires all action fields after a terminate flag; no undocumented early-stop rule is introduced.

## Why this matters on a robot

A vocabulary mismatch can map a plausible number into the wrong actuator field. Version the decoder and action codec together. Constraining syntax prevents illegal token IDs, but leaves semantic, collision and timing checks unresolved.

## Questions

Why does vocabulary order not break ties? Token identity, not list position, defines the declared deterministic choice. Can a forbidden logit change a legal probability? No; it is absent from the normalizer.

Source: [RT-2 output constraints](https://arxiv.org/html/2307.15818v1#S3.SS2). Prerequisite: [action grammar](/problems/rt2-parse-action-grammar). The supplied grammar and greedy tie rule are original teaching choices.
