---
{
  "schema_version": 1,
  "problem_id": "openvla-lora-policy-layer",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Add Low-Rank Adaptation to a Policy Layer",
  "summary": "Add Low-Rank Adaptation to a Policy Layer",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2024-openvla",
    "policy-interface"
  ],
  "paper_ids": [
    "2024-openvla"
  ],
  "paper_sections": [
    "Section 5.3: Parameter-Efficient Fine-Tuning",
    "LoRA low-rank weight update"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build",
    "dependencies": {
      "numpy": "2.2.4",
      "torch": "2.6.0+cpu"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.lora_policy_linear",
  "physical_contract": {
    "frames": [
      "Learned feature coordinates; no physical coordinate transform"
    ],
    "units": {
      "features": "dimensionless",
      "weights": "dimensionless"
    },
    "axes": "x(B,T,I), base_weight(O,I), adapter_down(r,I), adapter_up(O,r), output(B,T,O)",
    "timestamp_assumptions": "Same aligned observation context is supplied; no internal clock",
    "batching": "Nonempty bounded batch; exact axis bounds in statement"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-06,
    "atol": 1e-07,
    "exact_fields": [],
    "public_case_families": [
      "two-worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "typed-boundary-validation",
      "noncontiguous-inputs",
      "independent-oracle",
      "storage-and-nonmutation",
      "gradients-where-required",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded contract; source mechanisms and teaching deviations are explicit. No full trained policy or paper benchmark is reproduced.",
    "primary_urls": [
      "https://arxiv.org/html/2406.09246v3"
    ],
    "paper_card": "research/papers/vla-embodied/2024-openvla.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": [
    "curriculum_continuation"
  ]
}
---

# Add Low-Rank Adaptation to a Policy Layer

Implement lora_policy_linear(x, base_weight, adapter_down, adapter_up, alpha).

All four tensor inputs are finite CPU torch.float32 or torch.float64 tensors with a common dtype and absolute values <= 10. Shapes are x(B,T,I), base_weight(O,I), adapter_down(r,I), adapter_up(O,r). Require 1 <= B <= 32, 1 <= T <= 256, 1 <= I,O <= 256 and 1 <= r <= min(I,O,64). Each tensor and output must contain at most 1,000,000 entries. Noncontiguous tensors are valid. alpha is a built-in non-bool int/float in [0,64].

Return a fresh tensor y(B,T,O) with the input dtype/device, computed as x @ base_weight.T + (alpha/r) * ((x @ adapter_down.T) @ adapter_up.T). The supplied base_weight is frozen for this operation: no gradient may flow into it, even if it has requires_grad=True. Gradients must still flow through x in BOTH branches, and through both adapter matrices wherever they require gradients. With alpha=0 or a zero adapter matrix, retain the correct differentiable zero contributions; do not drop the autograd connection to a required adapter merely because its derivative is zero.

Preserve all input values, requires_grad settings and storage; do not mutate parameters, merge adapters into base_weight, or detach x. Non-tensor inputs raise TypeError; every other dtype/device/shape/value/alpha violation raises ValueError. The result must support backward in a grad-enabled call when x or either adapter requires gradients. The case where only the frozen base requires gradients does not require a differentiable output.

Features and weights are dimensionless learned coordinates. B and T are observation batches and token positions; no physical time step or coordinate transform is inferred. This is a single bias-free adapter calculation with explicit alpha/r scaling. Optimizer steps, dropout, quantization, parameter initialization, checkpoint merging and complete OpenVLA fine-tuning are outside scope.

## Implementation and evaluator plan

Review the complete mathematical and physical contract before implementation. Use independent scalar/tensor oracles, both worked examples, stated invalid-input behavior, aliasing checks and analytical gradients where applicable. Verify the reference through actual isolated Run and Submit and reject the starter before publication. No new runtime dependency or model checkpoint is needed.
