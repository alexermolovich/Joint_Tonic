# Parse and Validate an Action-Token Grammar

## Intuition

A robot output parser is an interface boundary. It must reject an unknown token or misplaced field rather than repairing the sequence by guessing. Parsing succeeds only when every channel retains a known meaning.

## Invert the declared map

Let vocabulary $v\in\mathbb Z^K$ contain unique action-token IDs, and let $T\in\mathbb Z^{B\times(D+1)}$ be candidate rows. The grammar is

$$
T_{b,0}\in\{0,1\},\qquad
T_{b,j+1}\in\{v_0,\ldots,v_{K-1}\}.
$$

When every row is valid, recover dimensionless bin indices and flags:

$$
Q_{b,j}=v^{-1}(T_{b,j+1}),\qquad s_b=T_{b,0}.
$$

B is the number of independent action examples, D is channel count, and K is vocabulary size. The inverse must return the position in the original vocabulary, not the ID's sorted rank.

## Visual: validation before decoding

| Candidate field | Token | Check | Result |
|---|---:|---|---|
| Termination | 0 | Member of {0,1} | Continue |
| Channel0 | 41 | In [41,7,99] at index0 | Bin0 |
| Channel1 | 99 | In [41,7,99] at index2 | Bin2 |

The row [0,41,99] decodes to [0,2]. Replacing99 with1 fails the action-field membership test even though1 is legal in the first column. The table is a static parser trace.

## Why this matters on a robot

Ignoring a missing or unknown channel shifts later values into the wrong actuator position. A parser should fail the whole batch under this contract, leaving recovery to a separate controller policy. Valid tokens still require physical bounds, units, timing and safety checks after decoding.

The grammar here is an original fixed-width teaching interface; RT-2 model variants use tokenizer-specific assignments. It is not a universal parser for arbitrary model text.

## Questions

Why reject duplicate vocabulary IDs? The inverse would be ambiguous. Does grammar validity prove a command is feasible? No; it establishes only a syntactically valid bin sequence.


## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2307.15818), Section3.2: action tokenization and valid output format. Prerequisites: [rt2-serialize-action-tokens](/problems/rt2-serialize-action-tokens).
