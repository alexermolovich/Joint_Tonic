# Serialize Robot Actions as Discrete Tokens

## Intuition

A quantized action bin is not automatically the ID of a language-model token. The encoder and decoder need a shared one-to-one mapping. A silently sorted vocabulary or assumed offset can turn a valid-looking output into a different action.

## Serialize fields without changing meaning

Let $Q\in\{0,\ldots,K-1\}^{B\times D}$ contain quantized action bins and let $v\in\mathbb Z^K$ be a supplied injective token map. B counts independent control examples, D ordered action channels and K bins. For termination flag $s_b\in\{0,1\}$, output $T\in\mathbb Z^{B\times(D+1)}$ is

$$
T_{b,0}=s_b,\qquad T_{b,j+1}=v_{Q_{b,j}}.
$$

Token IDs and bins are dimensionless integers. Physical units and frame conventions belong to the upstream codec. Our two reserved termination IDs and fixed field order are a teaching grammar, not a claim about the original pretrained tokenizer.

## Visual: preserve channel identity

| Field | Termination | Channel0 bin0 | Channel1 bin2 |
|---|---:|---:|---:|
| Input | 0 | 0 | 2 |
| Vocabulary lookup | unchanged | v[0]=41 | v[2]=99 |
| Output token | 0 | 41 | 99 |

The row becomes [0,41,99]. The vocabulary's numeric ordering is irrelevant. This table is a static serialization trace and text alternative.

## A reversible interface

Injectivity means $v^{-1}(v_q)=q$. Duplicate IDs would erase which bin was chosen, so they are rejected. Reserving0 and1 outside v separates the flag grammar from action fields; it does not make every well-formed sequence safe.

## Why this matters on a robot

A model checkpoint, tokenizer map and physical decoder must be versioned together. Reusing an old map with new action bounds can pass shape checks while moving the wrong joint. The termination flag also does not remove required fields from this fixed-width format.

## Questions

Why is vocabulary sorting wrong? It changes bin-to-token identity. Does termination1 permit fewer action fields? No; the complete fixed-width row is still required.


## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2307.15818), Section3.2: Robot-Action Fine-tuning. Prerequisites: [rt1-action-codec](/problems/rt1-action-codec).


## Numerical shape trace

| Field | Bin or flag | Serialized token |
|---|---:|---:|
| Termination | 0 | 0 |
| Action channel 0 | 0 | vocabulary[0] = 41 |
| Action channel 1 | 2 | vocabulary[2] = 99 |

With vocabulary [41,7,99], the complete row is [0,41,99].
