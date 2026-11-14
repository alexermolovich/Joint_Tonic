---
{
  "schema_version": 1,
  "problem_id": "octo-frozen-backbone-adaptation",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Add a Frozen-Backbone Adaptation Module",
  "summary": "Add a Frozen-Backbone Adaptation Module.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-octo",
    "policy-components"
  ],
  "paper_ids": [
    "2024-octo"
  ],
  "paper_sections": [
    "Original linear residual-adapter training step motivated by adapting generalist policies while freezing pretrained weights; this is not Octo official fine-tuning code or a full parameter-efficient method."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.adaptation_step",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed."
    },
    "axes": "Explicit token, batch and feature axes defined in the contract",
    "timestamp_assumptions": "Each batch row is a synchronized caller-supplied policy context; group order is explicit.",
    "batching": "Explicit token, batch and feature axes defined in the contract"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original linear residual-adapter training step motivated by adapting generalist policies while freezing pretrained weights; this is not Octo official fine-tuning code or a full parameter-efficient method.",
    "primary_urls": [
      "https://arxiv.org/abs/2405.12213"
    ],
    "paper_card": "research/papers/vla-embodied/2024-octo.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Add a Frozen-Backbone Adaptation Module

## Contract

features X real(B,E),1<=B<=128,1<=E<=64; base_weight W real(E,D),1<=D<=32; down A real(E,R), up C real(R,D),1<=R<=16; targets Y real(B,D); learning_rate real scalar0..1. Each array magnitude<=100. Return dict prediction float64(B,D) BEFORE update, loss Pythonfloat, down/up updated float64 arrays using one simultaneous gradient step on mean squared error over ALL B*D entries. Forward Z=XW+(XA)C. Freeze W and supplied X: update only A,C; use original A,C in both gradients, no sequential update. No nonlinearities, biases or optimizer state.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original linear residual-adapter training step motivated by adapting generalist policies while freezing pretrained weights; this is not Octo official fine-tuning code or a full parameter-efficient method.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
