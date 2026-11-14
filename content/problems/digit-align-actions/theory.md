# Align Tactile Frames with Robot Actions

## Intuition

A frame must be paired with a command that was already active when the image was captured. A future command can be closer in absolute time and still be the wrong cause of the observed contact.

## Mathematical mechanism

For frame time t and strictly increasing command times $s_j$, choose $$j^*(t)=\max\{j:s_j\le t\},\qquad a(t)=t-s_{j^*}.$$ The candidate is usable only when it exists and age a is at most the supplied limit. Retain the index and age of stale candidates for diagnosis, while returning zero aligned command for invalid rows. Missing predecessors use index -1 and NaN age. Time uses seconds on one clock; command channels are normalized dimensionless controller coordinates. This is a causal zero-order hold, not nearest-neighbor timestamp matching.

## Visual computation trace

| Frame time | Latest preceding command | Age | At limit 0.5 s |
|---|---|---|---|
| 0.5 s | 0 s | 0.5 s | valid |
| 1 s | 1 s | 0 s | valid |
| before first command | none | unknown | invalid |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Action times [0, 1], commands [[0.2], [0.8]], frame times [0.5, 1] and max_age 0.5 yield indices [0, 1], ages [0.5, 0], both valid, and aligned commands [[0.2], [0.8]].

## Why this matters on a robot

Lighting drift, elastomer wear and timing errors can resemble changed contact. A tactile image is an optical measurement; interpreting it as force without calibration can produce unsafe control decisions.

## Physical contract and limits

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

Source: [primary paper](https://arxiv.org/abs/2005.14679). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
