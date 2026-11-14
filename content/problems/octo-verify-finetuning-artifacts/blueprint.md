---
{
  "schema_version": 1,
  "problem_id": "octo-verify-finetuning-artifacts",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Verify Trainable Parameters and Fine-Tuning Artifacts",
  "summary": "Verify Trainable Parameters and Fine-Tuning Artifacts.",
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
    "Original deterministic artifact audit motivated by Octo adaptation and reproducibility; no weights are loaded, trained or serialized by this function."
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
  "entrypoint": "solution.verify_finetuning",
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
    "authoring_notes": "Original deterministic artifact audit motivated by Octo adaptation and reproducibility; no weights are loaded, trained or serialized by this function.",
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

# Verify Trainable Parameters and Fine-Tuning Artifacts

## Contract

parameters list<=256 of exact dicts name:str,shape:list of1..4 built-in positive ints<=10000,trainable:bool; product(shape)<=1e9, names unique ASCII dotted identifiers<=80chars. artifacts list<=256 exact dicts name:str,shape:list,base_sha256:str; names unique and must occur in parameters with identical shape. allowed_prefixes nonempty list<=16 unique dotted identifiers; matching means name==prefix or name starts prefix+dot (never raw textual prefix). base_sha256 exactly64lowercasehex. Return total_count int, trainable_count int, frozen_count int, unexpected_trainable sorted names, missing_artifacts sorted TRAINABLE names absent from artifacts, frozen_artifacts sorted supplied FROZEN names, mismatched_base sorted artifact names whose well-formed hash differs, and ready bool true iff all four lists empty. Unexpected trainability or differing valid hash are reported, not raised. Malformed structures/unknown artifacts/mismatched shape raise ValueError. Empty parameter list is allowed and ready if artifacts empty.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original deterministic artifact audit motivated by Octo adaptation and reproducibility; no weights are loaded, trained or serialized by this function.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
