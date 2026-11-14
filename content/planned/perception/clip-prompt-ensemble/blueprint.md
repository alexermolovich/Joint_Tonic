---
{
  "schema_version": 1,
  "problem_id": "clip-prompt-ensemble",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Build a Prompt-Ensembled Zero-Shot Classifier",
  "summary": "Build a Prompt-Ensembled Zero-Shot Classifier",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "perception"
  ],
  "topics": [
    "clip",
    "paper-component"
  ],
  "paper_ids": [
    "2021-clip"
  ],
  "paper_sections": [
    "Mechanism and conventions defined in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "clip-normalize-embeddings"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build",
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
  "entrypoint": "solution.prompt_ensemble_classifier",
  "physical_contract": {
    "frames": [
      "Explicit caller-observation conventions in statement"
    ],
    "units": {
      "features": "dimensionless"
    },
    "axes": "images(B,D),prompts(C,P,D); logits(B,C),prototypes(C,D).",
    "timestamp_assumptions": "One observation batch; no internal clock.",
    "batching": "images(B,D),prompts(C,P,D); logits(B,C),prototypes(C,D)."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 0.000001,
    "atol": 1e-7,
    "public_case_families": [
      "worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "validation",
      "edge-policy",
      "layout",
      "preservation",
      "independent-oracle",
      "scale"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching task. No copied source code or figure.",
    "primary_urls": [
      "https://arxiv.org/abs/2103.00020"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Build a Prompt-Ensembled Zero-Shot Classifier

## Contract

Implement prompt_ensemble_classifier(images, prompts, temperature). images and prompts are finite NumPy float64 arrays shaped(B,D),(C,P,D),1<=B<=256,1<=C<=1000,1<=P<=64,1<=D<=512; each array at most1,000,000 elements. Each image/prompt vector has L2 norm in[1e-6,1e6]. First normalize each prompt independently, average P unit prompts within each class, then normalize each class mean; reject a class mean with norm<1e-6. Normalize image rows and compute logits=unit_images @ prototypes.T / temperature. temperature is built-in int/float excluding bool in[1e-4,1e4]. Return new float64 (logits,prototypes), preserving inputs and noncontiguous support. TypeError for non-array inputs; ValueError for other violations. No softmax, tokenization, encoder, class-label output, or averaging raw unnormalized prompts. Rows/classes/prompt grouping preserve caller order. Features are dimensionless; each prompt group describes one class. This is inference prototype construction, not a gradient-based training API.

## Implementation and proof

Independent review precedes implementation. Test both examples and documented invalid/empty/layout cases; use independent objective/shape/value oracles. Verify actual isolated public Run and hidden Submit plus starter negative control. Reference and fixture code are original. Theory includes original math and static numerical/layout table with text alternative. No full-paper reproduction is claimed.
