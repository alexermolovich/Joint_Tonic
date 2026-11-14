# Roll Out Perturbed Control Sequences

Implement `rollout_controls(initial, transition, control_map, nominal, perturbations)`.

Roll out a batch of supplied control perturbations through a bounded discrete linear robot model.

`initial` is float64 `(D,)`, `transition` `(D,D)`, `control_map` `(D,U)`, `nominal` `(H,U)`, `perturbations` `(K,H,U)`, with `1<=D,U<=8`, `1<=H<=64`, `1<=K<=128`. State and control coordinates are normalized dimensionless features in a fixed caller-defined order. The matrices describe one fixed controller period already discretized by the caller; do not apply another timestep. Require the maximum absolute row sum of transition to be at most 1; absolute control_map entries at most 10; absolute initial, nominal and perturbation entries at most 100.

Return fresh float64 `controls (K,H,U)=nominal+perturbations` and `states (K,H+1,D)` in a dictionary. Every rollout starts from initial. For each k,t, compute `states[k,t+1]=transition@states[k,t]+control_map@controls[k,t]`. Do not clip commands or state, sample new noise, compute costs or alter the supplied perturbations. This original bounded linear teaching model illustrates MPPI rollout structure; it does not model the full nonlinear stochastic dynamics or importance-sampling correction of the paper.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Scalar A=B=1, initial `[0.]`, nominal `[[1.],[2.]]`, one zero perturbation sequence yield controls `[[[1.],[2.]]]` and states `[[[0.],[1.],[3.]]]`.
2. The same inputs with perturbation sequence `[[[1.],[-1.]]]` yield controls `[[[2.],[1.]]]` and states `[[[0.],[2.],[3.]]]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
