---
{
  "schema_version": 1,
  "problem_id": "octo-missing-modality-block-mask",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Build Block Masks for Missing Sensors and Goals",
  "summary": "Build Block Masks for Missing Sensors and Goals.",
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
    "Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy."
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
  "entrypoint": "solution.group_attention_mask",
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
    "authoring_notes": "Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.",
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

# Build Block Masks for Missing Sensors and Goals

## Contract

group_ids integer(L,),0<=L<=256; group_rules bool(G,G),1<=G<=16; present bool(B,L),1<=B<=16. IDs in0..G-1. Return bool(B,L,L): query i may read key j when group_rules[group_ids[i],group_ids[j]] and both positions are present. Rules are directed query-group by key-group. There is no extra temporal triangle or forced diagonal; callers encode their policy in group_rules. Entirely false query rows are permitted and must be skipped by a downstream attention operator.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
