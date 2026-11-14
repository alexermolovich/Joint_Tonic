# Subtract a Tactile Reference Image

## Intuition

Subtract a comparable unloaded reference to reveal optical change. Preserve the sign of channel differences, then summarize their absolute magnitude for thresholding inside a declared region of interest.

## Mathematical mechanism

For capture $I\in[0,1]^{B\times H\times W\times C}$, reference R and Boolean ROI M, $$\Delta_{buvc}=M_{uv}(I_{buvc}-R_{uvc}),\quad D_{buv}=\frac1C\sum_c|\Delta_{buvc}|,\quad A_{buv}=M_{uv}\land(D_{buv}>\tau).$$ Rows u increase down, columns v increase right, and tau is a dimensionless change threshold. Reference and captures must share alignment, exposure and optical calibration. The absolute value occurs before channel averaging; opposite signed channel changes must not cancel.

## Visual computation trace

| Pixel intensity | Reference | Signed change | Absolute change |
|---|---|---|---|
| 0.2 | 0.8 | -0.6 | 0.6 |
| outside ROI | any valid input | 0 | 0 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

For a zero one-channel reference, image [[0, 0.2], [0.1, 0.4]], an all-true ROI and threshold 0.15, the mask is [[False, True], [False, True]] and change equals the input image.

## Why this matters on a robot

Lighting drift, elastomer wear and timing errors can resemble changed contact. A tactile image is an optical measurement; interpreting it as force without calibration can produce unsafe control decisions.

## Physical contract and limits

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

Source: [primary paper](https://arxiv.org/abs/2005.14679). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
