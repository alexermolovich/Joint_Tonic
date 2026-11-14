# Validate a Tactile Image Capture Contract

## Intuition

A usable tactile frame needs reliable capture metadata as well as pixels. Report clock gaps, dropped identifiers, changed exposure and optical saturation separately so an operator can identify the failing part of the capture pipeline.

## Mathematical mechanism

For successive timestamps t and frame IDs n, flag bad timing when $t_i-t_{i-1}\le0$ or when the gap exceeds g; flag continuity when $n_i-n_{i-1}\ne1$. For exposure e and declared baseline $e_*$, $$b_e=\mathbf1[|e-e_*|>0.05e_*],\quad s=\frac1{3HW}\sum_{u,v,c}\mathbf1[I_{uvc}\in\{0,255\}].$$ Saturation is flagged only when s>0.95. The first row has no predecessor and gets false timing/ID flags. Exposures use microseconds, timestamp gaps seconds, and s is a dimensionless channel fraction. These thresholds are original operational heuristics; saturation is not a contact classifier.

## Visual computation trace

| Check | Evidence | Flag condition |
|---|---|---|
| Timing | consecutive capture times | nonpositive or excessive gap |
| IDs | consecutive frame identifiers | increment differs from one |
| Exposure | measured versus baseline | relative difference exceeds 5% |
| Saturation | channels at 0 or 255 | fraction exceeds 95% |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

One RGB frame [128, 128, 128] of size 1 by 1, timestamp 0, ID 0, exposure 1000 and expected exposure 1000 yields no flags, usable [True], saturation fraction [0] and ready True.

## Why this matters on a robot

Lighting drift, elastomer wear and timing errors can resemble changed contact. A tactile image is an optical measurement; interpreting it as force without calibration can produce unsafe control decisions.

## Physical contract and limits

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

Source: [primary paper](https://arxiv.org/abs/2005.14679). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
