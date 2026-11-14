---
{
  "schema_version": 1,
  "problem_id": "palm-e-multimodal-causal-mask",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Build a Multimodal Causal Attention Mask",
  "summary": "Putting sensors into a language sequence must not let a prediction read future tokens.",
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
    "Original dense causal-mask component for a PaLM-E-style interleaved sequence. This declares ordinary autoregressive causality, not bidirectional vision blocks or a full model attention implementation."
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
  "entrypoint": "solution.multimodal_causal_mask",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "All axes are token positions and dimensionless modality identifiers; no actuator units."
    },
    "axes": "modalities(L), present(B,L) -> allowed(B,L,L)",
    "timestamp_assumptions": "Sequence order defines causality. Tokens may describe multiple sensors but callers must synchronize them before this function.",
    "batching": "modalities(L), present(B,L) -> allowed(B,L,L)"
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
    "authoring_notes": "Original dense causal-mask component for a PaLM-E-style interleaved sequence. This declares ordinary autoregressive causality, not bidirectional vision blocks or a full model attention implementation.",
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

# Build a Multimodal Causal Attention Mask

## Contract

`multimodal_causal_mask(modalities,present)` receives integer modalities(L,) with IDs0=image,1=state,2=text,0<=L<=256, and present:bool(B,L),1<=B<=16. Return bool(B,L,L), True means query row i may read key column j exactly when i>=j and both tokens are present in that batch. Modalities validate the token schema but do not override causality. Missing query rows are entirely false, including diagonal. Empty L is allowed; no special always-visible token is added.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original dense causal-mask component for a PaLM-E-style interleaved sequence. This declares ordinary autoregressive causality, not bidirectional vision blocks or a full model attention implementation.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
