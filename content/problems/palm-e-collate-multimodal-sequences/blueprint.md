---
{
  "schema_version": 1,
  "problem_id": "palm-e-collate-multimodal-sequences",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Collate Variable Multimodal Sequences",
  "summary": "Different observations can produce different token counts.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-palm-e",
    "policy-components"
  ],
  "paper_ids": [
    "2023-palm-e"
  ],
  "paper_sections": [
    "Original collator for PaLM-E-style multimodal embeddings. It does not tokenize text, encode images or insert supervision labels."
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
  "entrypoint": "solution.collate_multimodal",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Features are projected dimensionless embeddings; modality codes0image/1state/2text carry no physical units."
    },
    "axes": "B sequences(Li,E) -> padded tokens(B,Lmax,E), masks/IDs(B,Lmax), lengths(B)",
    "timestamp_assumptions": "Each example retains its supplied token order; no cross-example temporal relationship is implied.",
    "batching": "B sequences(Li,E) -> padded tokens(B,Lmax,E), masks/IDs(B,Lmax), lengths(B)"
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
    "authoring_notes": "Original collator for PaLM-E-style multimodal embeddings. It does not tokenize text, encode images or insert supervision labels.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.03378"
    ],
    "paper_card": "research/papers/vla-embodied/2023-palm-e.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Collate Variable Multimodal Sequences

## Contract

`collate_multimodal(sequences,modalities)` takes two nonempty Python lists of equal length B,1<=B<=32. Each sequence is real(Li,E),0<=Li<=256, common1<=E<=128; each modality array is integer(Li,) in0..2. Return dict tokens:float64(B,Lmax,E) right-padded0, modalities:int64(B,Lmax) right-padded-1, present:bool(B,Lmax) and lengths:int64(B,). Empty examples and an all-empty batch are allowed; E remains supplied by their (0,E) shapes. No truncation or sequence sorting. The total padded token output must contain at most1,000,000 entries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original collator for PaLM-E-style multimodal embeddings. It does not tokenize text, encode images or insert supervision labels.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
