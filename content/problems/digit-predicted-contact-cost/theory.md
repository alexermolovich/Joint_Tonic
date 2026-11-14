# Score Predicted Tactile Contact Outcomes

## Intuition

Candidate tactile predictions can be compared with a desired image before choosing a command. Separate appearance error from supplied action effort, and keep invalid candidates out of selection instead of assigning them an attractive zero score.

## Mathematical mechanism

For candidate prediction $\hat I_k$, goal G and nonempty Boolean ROI M, define $$E_k=\frac{\sum_{u,v,c}M_{uv}(\hat I_{kuvc}-G_{uvc})^2}{C\sum_{u,v}M_{uv}},\qquad J_k=E_k+\lambda e_k.$$ Intensities, supplied effort e and total cost are dimensionless under the declared normalization. Choose the smallest valid cost, breaking exact ties by original candidate index. Invalid candidates report NaN and cannot win. These supplied predictions may be wrong; optimizing their score does not validate the learned dynamics or physical contact.

## Visual computation trace

| Candidate | Image MSE | Effort | Weight | Cost |
|---|---|---|---|---|
| 0 | 0 | 1 | 0.2 | 0.2 |
| 1 | 1 | 0 | 0.2 | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Two single-pixel predictions 0 and 1, goal 0, efforts [1, 0], weight 0.2 and both candidates valid yield image errors [0, 1], costs [0.2, 1] and best index 0.

## Why this matters on a robot

Lighting drift, elastomer wear and timing errors can resemble changed contact. A tactile image is an optical measurement; interpreting it as force without calibration can produce unsafe control decisions.

## Physical contract and limits

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

Source: [primary paper](https://arxiv.org/abs/2005.14679). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
