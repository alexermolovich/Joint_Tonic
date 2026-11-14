# Collate Variable Multimodal Sequences

## Intuition

Different observations can produce different token counts. Padding makes one rectangular batch, but explicit lengths and presence masks must distinguish real zero-valued features from unused storage.

## Mathematical mechanism

Let 

$$L_{max}=\max_bL_b$$

. For $i<L_b$, copy $X_{b,i,:}$ into Y; otherwise set $Y_{b,i,:}=0$. Presence is $P_{bi}=\mathbf1[i<L_b]$, and padded modality ID is -1. This preserves an actual all-zero token as present. B counts examples, E is shared embedding width, and Li counts source tokens.

## Visual computation trace

| Example | Source length | Padded tokens | Presence |
|---|---|---|---|
| 0 | 2 | [1,2] | [true,true] |
| 1 | 1 | [3,0] | [true,false] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

sequences=[[[1],[2]],[[3]]], modalities=[[0,2],[1]] returns tokens=[[[1],[2]],[[3],[0]]], modalities=[[0,2],[1,-1]], present=[[True,True],[True,False]], lengths=[2,1].

## Why this matters on a robot

Using feature values to infer padding drops legitimate zero embeddings. Sorting by length without returning an inverse permutation also separates action labels from their observations. This contract preserves example order and requires all masked-out source data to be valid.

## Physical contract and limits

Features are projected dimensionless embeddings; modality codes0image/1state/2text carry no physical units. Each example retains its supplied token order; no cross-example temporal relationship is implied. Original collator for PaLM-E-style multimodal embeddings. It does not tokenize text, encode images or insert supervision labels.

Source: [primary paper](https://arxiv.org/abs/2303.03378). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
