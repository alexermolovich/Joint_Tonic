---
{
  "schema_version": 1,
  "problem_id": "palm-e-interleave-modal-tokens",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Interleave Image, State, and Text Tokens",
  "summary": "A language model can consume image, state and text embeddings in one sequence when they share a feature width.",
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
    "Original explicit interleaver motivated by PaLM-E embedding continuous observations into a language stream. It assumes the sensor projections and tokenizer already ran."
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
  "entrypoint": "solution.interleave_modal_tokens",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Projected token features are dimensionless; IDs are indices, not physical channels."
    },
    "axes": "three source matrices(Ni/E,Ns/E,Nt/E), layout(L,2) -> tokens(L,E), modalities(L)",
    "timestamp_assumptions": "All source arrays belong to one caller-aligned observation context; ordering is supplied, not inferred from timestamps.",
    "batching": "three source matrices(Ni/E,Ns/E,Nt/E), layout(L,2) -> tokens(L,E), modalities(L)"
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
    "authoring_notes": "Original explicit interleaver motivated by PaLM-E embedding continuous observations into a language stream. It assumes the sensor projections and tokenizer already ran.",
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

# Interleave Image, State, and Text Tokens

## Contract

`interleave_modal_tokens(image,state,text,layout)` receives three real matrices (Ni,E),(Ns,E),(Nt,E), 0<=eachN<=512, common1<=E<=128; layout integer(L,2),0<=L<=1024. Each row contains (kind,index): kind0=image,1=state,2=text; index must address that source. Return (tokens:float64(L,E), modalities:int64(L,)). Preserve layout order and permit repeated source rows. Empty layout returns correctly shaped empty outputs. Empty source is allowed only when no layout row addresses it. No padding, projection, positional embeddings or automatic special token is inserted.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original explicit interleaver motivated by PaLM-E embedding continuous observations into a language stream. It assumes the sensor projections and tokenizer already ran.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
