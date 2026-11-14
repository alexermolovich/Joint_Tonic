# Build a Multimodal Causal Attention Mask

## Intuition

Putting sensors into a language sequence must not let a prediction read future tokens. A padding or missing-sensor token should be neither a source of information nor an active query.

## Mathematical mechanism

For batch b and positions i,j, let $P_{bi}$ be the Boolean presence mask. Define $$A_{bij}=P_{bi}\land P_{bj}\land(j\leq i).$$ A is the allowed-attention tensor, not additive logits. Modality IDs only validate the source type. A completely absent query has no allowed key; a downstream softmax must handle or skip that row rather than normalizing all negative infinity.

## Visual computation trace

| Query/key | image0 | absent state1 | text2 |
|---|---|---|---|
| image0 | true | false | false |
| absent state1 | false | false | false |
| text2 | true | false | true |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

modalities=[0,1,2], present=[[True,False,True]] returns [[[True,False,False],[False,False,False],[True,False,True]]].

## Why this matters on a robot

Masking only keys leaves meaningless query rows active. Flipping the triangular direction leaks future action tokens into training and can produce deceptively low loss. An all-false row is a declared downstream concern, not permission to unmask padding.

## Physical contract and limits

All axes are token positions and dimensionless modality identifiers; no actuator units. Sequence order defines causality. Tokens may describe multiple sensors but callers must synchronize them before this function. Original dense causal-mask component for a PaLM-E-style interleaved sequence. This declares ordinary autoregressive causality, not bidirectional vision blocks or a full model attention implementation.

Source: [primary paper](https://arxiv.org/abs/2303.03378). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
