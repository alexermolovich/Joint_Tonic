---
{
  "schema_version": 1,
  "problem_id": "clip-prompt-class-drift",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Detect Prompt and Class Distribution Drift",
  "summary": "Separate changed text prototypes from changed predicted-class frequencies.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "clip",
    "clip-prompt-class-drift"
  ],
  "paper_ids": [
    "2021-clip"
  ],
  "paper_sections": [
    "Zero-shot classification via text prototypes; original deployment drift diagnostics"
  ],
  "track_ids": [
    "paper-2021-clip"
  ],
  "prerequisite_problem_ids": [
    "clip-prompt-ensemble"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.prompt_class_drift",
  "physical_contract": {
    "frames": [
      "Fixed text-encoder class coordinate system"
    ],
    "units": {
      "values": "dimensionless features and counts"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "3b9c6e04d6d30fa798ac9320e7ef839e579c62637430762749bf3caf44e9cbad"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2103.00020"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Detect Prompt and Class Distribution Drift

Implement `prompt_class_drift(old_prototypes: np.ndarray, new_prototypes: np.ndarray, old_counts: np.ndarray, new_counts: np.ndarray) -> tuple[np.ndarray, float]`.

Separate changed text prototypes from changed predicted-class frequencies.
old_prototypes and new_prototypes are float64(C,D),1<=C<=256,1<=D<=512; each row norm>=1e-8. Rows refer to the same ordered classes and same encoder version. old_counts,new_counts are int64(C,) nonnegative<=1000000, each with positive total. Return float64(C,) cosine distances `1-dot(normalize(old),normalize(new))`, clipped into [0,2], and Python float Jensen-Shannon divergence between normalized count histograms, using natural logs and 0*log(0)=0. Counts describe comparable observation windows, not necessarily equal sample counts. No pseudocount smoothing, class remapping, or causal attribution. Changing class inventory requires a new contract upstream.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Old prototypes `[[1,0],[0,1]]`, new `[[1,0],[1,0]]` give distances `[0,1]`. Counts `[1,0]` versus `[0,1]` give JS=ln(2).
2. Multiplying every prototype by a positive scale and counts `[1,3]` to `[2,6]` gives zero drift in both outputs: directions and proportions are unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/2103.00020). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Normalize embeddings/counts, compute per-class cosine distance and two masked KL terms. O(CD) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
