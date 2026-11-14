# Estimate Contact Patch Statistics

## Intuition

A contact candidate mask can be summarized by its area, center and spread in the image. These are geometric image statistics, so preserve pixel conventions and explicitly mark an absent region rather than inventing a center.

## Mathematical mechanism

Let $S_b=\{(x,y):M_{byx}=1\}$ contain selected pixel centers. For $n_b=|S_b|>0$, $$\mu_b=\frac1{n_b}\sum_{p\in S_b}p,\qquad\Sigma_b=\frac1{n_b}\sum_{p\in S_b}(p-\mu_b)(p-\mu_b)^T.$$ The mean orders x before y; covariance uses the population divisor n. Coordinates are pixels, covariance pixels squared, and area a pixel count. Bounds are integer min coordinates and max coordinates plus one. Empty masks have unknown mean/covariance and bounds -1. No connected-component split or force conversion occurs.

## Visual computation trace

| Selected centers (x,y) | Centroid | Population covariance |
|---|---|---|
| (1,0), (1,1) | (1,0.5) | diag(0,0.25) |
| none | unknown | unknown |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Mask [[False, True], [False, True]] yields area 2, centroid [1, 0.5], covariance [[0, 0], [0, 0.25]] and bounds [1, 0, 2, 2].

## Why this matters on a robot

Lighting drift, elastomer wear and timing errors can resemble changed contact. A tactile image is an optical measurement; interpreting it as force without calibration can produce unsafe control decisions.

## Physical contract and limits

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

Source: [primary paper](https://arxiv.org/abs/2005.14679). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
