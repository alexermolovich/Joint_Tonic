# Quantify Calibration Sensitivity

Implement calibration_sensitivity(baseline, plus, minus, delta, scales) -> dict.

baseline is NumPy float64(M,), plus and minus float64(K,M), delta and scales float64(K,),1<=K<=64,1<=M<=64. All values finite; baseline/plus/minus in[-1e6,1e6], delta and scales in[1e-6,1e6]. Each metric is a comparable dimensionless performance score; parameter j uses its caller-declared physical unit, and both delta[j] and scales[j] use that same unit. plus[j]/minus[j] are matched evaluations after changing only parameter j by ±delta[j] about one nominal calibration. scales[j] is a physical uncertainty scale.

Return float64(K,M) slope=(plus-minus)/(2*delta[:,None]), curvature=(plus-2*baseline[None,:]+minus)/(delta[:,None]**2), scaled_sensitivity=abs(slope)*scales[:,None], and ranking:int64(K,), sorted by descending max scaled_sensitivity per parameter, breaking exact ties by smaller input index. Preserve inputs and return independent arrays; noncontiguous inputs valid. Invalid contracts raise ValueError. No parameter names or perturbations are inferred; no simulator runs occur.

Slope units are score per physical-unit, curvature score per physical-unit squared, scaled sensitivity dimensionless. These finite differences are a local diagnostic, not a global robustness bound or proof that the parameter perturbations are physically valid.

## Worked examples

### Angular calibration perturbation
baseline[0.5], plus[[0.8]], minus[[0.4]], delta[0.1], scales[0.02] returns slope[[2]], curvature[[20]], scaled_sensitivity[[0.04]], ranking[0].

### Stable deterministic tie
baseline[0], plus[[2],[4]], minus[[-2],[-4]], delta[1,2], scales[1,1] returns slope[[2],[2]], curvature[[0],[0]], scaled_sensitivity[[2],[2]], ranking[0,1].

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
