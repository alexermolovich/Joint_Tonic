# Add Low-Rank Adaptation to a Policy Layer

Implement lora_policy_linear(x, base_weight, adapter_down, adapter_up, alpha).

All four tensor inputs are finite CPU torch.float32 or torch.float64 tensors with a common dtype and absolute values <= 10. Shapes are x(B,T,I), base_weight(O,I), adapter_down(r,I), adapter_up(O,r). Require 1 <= B <= 32, 1 <= T <= 256, 1 <= I,O <= 256 and 1 <= r <= min(I,O,64). Each tensor and output must contain at most 1,000,000 entries. Noncontiguous tensors are valid. alpha is a built-in non-bool int/float in [0,64].

Return a fresh tensor y(B,T,O) with the input dtype/device, computed as x @ base_weight.T + (alpha/r) * ((x @ adapter_down.T) @ adapter_up.T). The supplied base_weight is frozen for this operation: no gradient may flow into it, even if it has requires_grad=True. Gradients must still flow through x in BOTH branches, and through both adapter matrices wherever they require gradients. With alpha=0 or a zero adapter matrix, retain the correct differentiable zero contributions; do not drop the autograd connection to a required adapter merely because its derivative is zero.

Preserve all input values, requires_grad settings and storage; do not mutate parameters, merge adapters into base_weight, or detach x. Non-tensor inputs raise TypeError; every other dtype/device/shape/value/alpha violation raises ValueError. The result must support backward in a grad-enabled call when x or either adapter requires gradients. The case where only the frozen base requires gradients does not require a differentiable output.

Features and weights are dimensionless learned coordinates. B and T are observation batches and token positions; no physical time step or coordinate transform is inferred. This is a single bias-free adapter calculation with explicit alpha/r scaling. Optimizer steps, dropout, quantization, parameter initialization, checkpoint merging and complete OpenVLA fine-tuning are outside scope.

## Worked examples

## A rank-one update changes the forward value

For x=[[[1,2]]], base_weight=[[1,0],[0,1]], adapter_down=[[1,-1]], adapter_up=[[2],[3]], alpha=2, use one common floating tensor dtype. The low-rank hidden value is -1. The scaled update is [-4,-6], so return [[[-3,-4]]]. For the sum of outputs, the x gradient is [[[11,-9]]]; base_weight receives no gradient.

## A zero up-projection preserves the base prediction

For x=[[[3,4]]], base_weight=[[2,0],[0,-1]], adapter_down=[[1,1]], adapter_up=[[0],[0]], alpha=1, return [[[6,-4]]]. The adapter_down gradient is zero at this point, but each adapter_up entry has gradient 7 for the sum of outputs. A zero initial adapter update does not mean all adapter learning is disabled.


# Worked examples

## A rank-one update changes the forward value

For x=[[[1,2]]], base_weight=[[1,0],[0,1]], adapter_down=[[1,-1]], adapter_up=[[2],[3]], alpha=2, use one common floating tensor dtype. The low-rank hidden value is -1. The scaled update is [-4,-6], so return [[[-3,-4]]]. For the sum of outputs, the x gradient is [[[11,-9]]]; base_weight receives no gradient.

## A zero up-projection preserves the base prediction

For x=[[[3,4]]], base_weight=[[2,0],[0,-1]], adapter_down=[[1,1]], adapter_up=[[0],[0]], alpha=1, return [[[6,-4]]]. The adapter_down gradient is zero at this point, but each adapter_up entry has gradient 7 for the sum of outputs. A zero initial adapter update does not mean all adapter learning is disabled.
