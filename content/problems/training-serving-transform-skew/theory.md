# Theory: compare the same observation at the transform boundary

## Intuition

A model can receive different inputs after deployment even when its weights are unchanged. A serving preprocessor may use a stale normalization scale, a different channel order, or different calibration. Comparing paired transformed observations isolates this boundary before model predictions obscure the cause.

The rows must actually be paired. Comparing unrelated frames tests scene variation as well as preprocessing and cannot establish parity.

## A per-feature numerical contract

Let $X,Y\in\mathbb R^{N\times D}$ be training and serving feature matrices. $N$ counts aligned observations; $D$ counts features in their declared column order. Each column has its own physical unit and frame convention, identical between $X$ and $Y$. Define absolute errors and permitted differences:

$$
e_{ij}=|Y_{ij}-X_{ij}|,\qquad
t_{ij}=a_j+r|X_{ij}|.
$$

Here $a\in\mathbb R_{\ge0}^{D}$ is the supplied absolute-tolerance vector, with the same units as each feature; $r\in[0,1]$ is a dimensionless relative tolerance. Both $e_{ij}$ and $t_{ij}$ have that feature's units. Emit a failure exactly when

$$
m_{ij}=\mathbf 1[e_{ij}>t_{ij}]=1.
$$

Absolute tolerance protects values near zero, where a relative term vanishes. Relative tolerance allows a scale-proportional difference. This is an explicit engineering tolerance, not a learned statistical confidence interval.

The training-side magnitude is intentional. Swapping $X$ and $Y$ changes the threshold, so a general symmetric distance function is not automatically a valid implementation.

## Visual: shared inputs, separate transforms

~~~mermaid
flowchart LR
  O["Same captured observations"] --> T["Training transform"]
  O --> S["Serving transform"]
  T --> X["X: N by D"]
  S --> Y["Y: N by D"]
  X --> C["Compare paired cells"]
  Y --> C
  C --> M["Row-major mismatch locations"]
~~~

**Text alternative:** identical observations enter both transform paths. Their aligned feature matrices enter one comparison, which reports locations rather than silently averaging errors. Static diagram; no animation.

For worked example 1, both absolute tolerances are 0.125:

| Row | Feature | Error | Allowed | Fail? |
|---|---|---:|---:|---|
| 0 | depth_m | 0.125 m | 0.125 m | no |
| 0 | yaw_rad | 0.25 rad | 0.125 rad | yes |
| 1 | depth_m | 0.5 m | 0.125 m | yes |
| 1 | yaw_rad | 0.125 rad | 0.125 rad | no |

The output is [(0, "yaw_rad"), (1, "depth_m")]. Averaging these columns would mix metres and radians and could hide a failing feature.

## Why this matters on a robot

Depth normalization or action scaling can change the physical meaning of model inputs. A parity replay helps catch a deployed transform diverging from training. But both paths can be identically wrong, and numerically equal arrays can still carry inconsistent schema labels. Store transform/calibration versions and separately validate units, coordinate frames, and observation identity.

TFX discusses keeping training and serving transformations consistent; the tolerance and report format here are our exercise contract. [TFX, data transformation](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Questions

1. Why is a relative tolerance alone ineffective for a zero-valued training feature?
2. Does an empty mismatch list prove the robot's feature schema is correct?

Prerequisite: understand that raw robot observations are transformed before model inference. No statistical-distribution lesson is required.
