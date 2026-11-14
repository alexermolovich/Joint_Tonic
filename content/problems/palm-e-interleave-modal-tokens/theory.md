# Interleave Image, State, and Text Tokens

## Intuition

A language model can consume image, state and text embeddings in one sequence when they share a feature width. An explicit layout makes the sequence order testable instead of hiding it inside string replacement or concatenation conventions.

## Mathematical mechanism

Let source matrices be $X^{(g)}\in\mathbb R^{N_g\times E}$ for modality g in {0,1,2}. A layout row $(g_l,i_l)$ selects 

$$Y_l=X^{(g_l)}_{i_l}$$

, giving $Y\in\mathbb R^{L\times E}$ and modality trace $m_l=g_l$. E is feature width and L final sequence length. Equal width does not establish semantic correspondence: the caller chooses each source index explicitly.

## Visual computation trace

| Layout row | Source | Emitted token |
|---|---|---|
| (2,0) | text0 | [5,6] |
| (0,0) | image0 | [1,2] |
| (1,0) | state0 | [3,4] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

image=[[1,2]], state=[[3,4]], text=[[5,6]], layout=[[2,0],[0,0],[1,0]] returns tokens=[[5,6],[1,2],[3,4]], modalities=[2,0,1].

## Why this matters on a robot

Concatenating source groups in a fixed order ignores the prompt’s intended context positions. Equal feature widths do not compensate for stale sensor data or different image preprocessing. Keep the layout and preprocessing version with each training example.

## Physical contract and limits

Projected token features are dimensionless; IDs are indices, not physical channels. All source arrays belong to one caller-aligned observation context; ordering is supplied, not inferred from timestamps. Original explicit interleaver motivated by PaLM-E embedding continuous observations into a language stream. It assumes the sensor projections and tokenizer already ran.

Source: [primary paper](https://arxiv.org/abs/2303.03378). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
