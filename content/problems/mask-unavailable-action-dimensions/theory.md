# Mask Unavailable Action Dimensions

## Intuition

A common tensor width can include channels that a particular robot does not possess. Missing a wrist axis is different from commanding its velocity to zero. Use availability metadata to replace placeholders, then keep the mask beside the data.

## Select rather than multiply

Let $A\in\mathbb R^{B\times D}$ store action values and $M\in\{0,1\}^{B\times D}$ indicate availability. The cleaned tensor is

$$
Y_{b,d}=\begin{cases}A_{b,d},&M_{b,d}=1,\\0,&M_{b,d}=0.\end{cases}
$$

B indexes independent robot examples and D ordered channels. Each retained value keeps its own declared unit and frame. The piecewise definition matters for nonfinite placeholders: IEEE floating-point $0\cdot\mathrm{NaN}$ is not zero.

## Visual: one row, three meanings

| Channel | Stored value | Available | Cleaned value |
|---|---:|---|---:|
| 0 | NaN | false | 0 |
| 1 | 0 | true | 0 |
| 2 | infinity | false | 0 |

All outputs are zero, but only channel1 is a valid recorded action. The table is the original static visual and text alternative.

## Why this matters on a robot

Supervising nonexistent joints as zero teaches a different objective from excluding them. Conversely, discarding a supported zero action loses real pause or hold behavior. Later losses must use availability, and downstream decoders must still respect robot-specific channels and control modes.

## Questions

1. Why is actions*available unsafe for the second example?
2. Does a zero in the output prove a channel was absent?

## Sources and prerequisites

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864), SectionIV data consolidation and SectionV cross-embodiment evaluation. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

