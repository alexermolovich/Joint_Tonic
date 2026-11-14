# Map Text Tokens to Grounded Phrases

## Intuition

Text encoders operate on tokens while instructions refer to phrases. Character offsets provide a stable bridge, including when one token overlaps only part of a phrase.

## Math and interval trace

Token $t$ occupies half-open interval $[a_t,b_t)$ and phrase $p$ occupies $[s_p,e_p)$ in Unicode code-point indices. The positive map is
$$M_{pt}=\mathbf1[\max(s_p,a_t)<\min(e_p,b_t)].$$
Its shape is $P\times T$ and values are boolean. Empty token intervals have no positive-length intersection and therefore never match. No positional sorting is required because rows and columns preserve caller identities.

| Token interval | Phrase interval | Intersection | Match |
|---|---|---|---|
| [2,5) | [4,6) | [4,5) | true |
| [2,5) | [5,6) | empty | false |
| [0,0) | [0,3) | empty | false |

The strict inequality is essential: replacing it with ≤ attaches boundary-touching tokens and special tokens to phrases. This matrix is an alignment input, not a calibrated phrase probability.

## Why this matters on a robot

Misaligned noun phrases can attach a strong box score to the wrong object name. Byte offsets mixed with Unicode code-point offsets break on non-ASCII instructions. Preserve the original text and tokenizer offset convention; a box detector cannot repair incorrect language metadata.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
