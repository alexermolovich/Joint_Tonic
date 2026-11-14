# Normalize and Mask Embodiment-Specific Action Spaces

## Intuition

A shared model can reserve channels that some robots do not possess. Normalize observed channels using embodiment-specific statistics and separately report which entries are real supervision.

## Mathematical mechanism

With action A, mean mu, positive scale sigma and availability M, $$Z_{bhd}=\begin{cases}(A_{bhd}-\mu_{bd})/\sigma_{bd}&M_{bd}=1\\0&M_{bd}=0.\end{cases}$$ The supervision mask is $V_{bhd}=M_{bd}$. B indexes embodiments/examples, H future timesteps, D shared action channels. A zero normalized value can be valid; only V identifies missing channels.

## Visual computation trace

| Channel | Action | Mean/std | Available | Output |
|---|---|---|---|---|
| arm | 3 | 1/2 | true | 1 |
| absent gripper | 9 | 0/1 | false | 0 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

actions=[[[3,9],[5,8]]], available=[[True,False]], mean=[[1,0]], std=[[2,1]] returns normalized=[[[1,0],[2,0]]] and mask=[[[True,False],[True,False]]].

## Why this matters on a robot

Applying another robot’s statistics can shift or saturate commands after decoding. An unavailable channel must not contribute to a loss just because its stored normalized value is zero. Statistics, channel names, frames and calibration versions belong with the checkpoint.

## Physical contract and limits

Each action channel retains its declared controller unit in inputs; per-channel mean/std use that unit, output is dimensionless. H is an equally spaced action horizon supplied by the dataset; normalization does not change timing or controller frames. Original normalization/masking component inspired by OXE cross-embodiment learning. Missing dimensions are masked, not treated as observed zero commands.

Source: [primary paper](https://arxiv.org/abs/2310.08864). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
