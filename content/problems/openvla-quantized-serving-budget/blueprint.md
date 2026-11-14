---
{
  "schema_version": 1,
  "problem_id": "openvla-quantized-serving-budget",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Estimate Memory, Latency, and Quantized Serving Budgets",
  "summary": "Estimate Memory, Latency, and Quantized Serving Budgets.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-openvla",
    "policy-components"
  ],
  "paper_ids": [
    "2024-openvla"
  ],
  "paper_sections": [
    "Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied."
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
  "entrypoint": "solution.serving_budget",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Memory bytes; latency/deadline milliseconds; parameter and token counts dimensionless."
    },
    "axes": "Explicit batch, sequence and channel axes defined in the contract",
    "timestamp_assumptions": "Caller-synchronized observations; generation time and physical control time are distinct.",
    "batching": "Explicit batch, sequence and channel axes defined in the contract"
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
    "authoring_notes": "Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.",
    "primary_urls": [
      "https://arxiv.org/abs/2406.09246"
    ],
    "paper_card": "research/papers/vla-embodied/2024-openvla.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Estimate Memory, Latency, and Quantized Serving Budgets

## Contract

parameter_count built-in integer1..10^12; bits integer vector(C,) values4,8,16,32,1<=C<=128; overhead_bytes and kv_bytes integer(C,), each0..1e6; latency_ms real(C,K),1<=K<=4096, strictly positive. memory_limit built-in integer0..10^13; deadline_ms realpositive<=1e6. Packed weight bytes=ceil(parameter_count*bits/8), no assumed speedup from quantization. Add supplied overhead and KV cache. p95 latency nearest rank ceil(.95*K)-1. Return weight_bytes/total_bytes int64(C,), p95_latency_ms float64(C,), feasible bool(C,) requiring total<=limit AND p95<=deadline. This excludes unspecified activations and training optimizer memory; supply overhead appropriate for this teaching budget.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
