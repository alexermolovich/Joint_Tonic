---
{
  "schema_version": 1,
  "problem_id": "dinov2-camera-feature-drift",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Monitor Frozen-Feature Drift Across Camera Domains",
  "summary": "Compare frozen-feature channel means using a reference-domain scale.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "dinov2",
    "dinov2-camera-feature-drift"
  ],
  "paper_ids": [
    "2023-dinov2"
  ],
  "paper_sections": [
    "Frozen visual representation evaluation; original camera-domain feature monitoring"
  ],
  "track_ids": [
    "paper-2023-dinov2"
  ],
  "prerequisite_problem_ids": [],
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
  "entrypoint": "solution.feature_drift",
  "physical_contract": {
    "frames": [
      "Fixed encoder feature coordinates"
    ],
    "units": {
      "values": "dimensionless frozen features"
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
    "evaluator_sha256": "b186d06134b2c9cfa1ccab39222b6c09bd396b105e3193901fab5880c5f22232"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.07193"
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

# Monitor Frozen-Feature Drift Across Camera Domains

Implement `feature_drift(reference: np.ndarray, current: np.ndarray) -> tuple[np.ndarray, float]`.

Compare frozen-feature channel means using a reference-domain scale.
Inputs reference (N,D) and current (M,D) float64 contain dimensionless embeddings from the SAME frozen encoder/preprocessing,1<=N,M<=4096,1<=D<=256. Compute population reference variance (divide by N), then per-channel shift `z=(mean(current)-mean(reference))/sqrt(var(reference)+1e-6)`. Return fresh float64(D,) z and Python float score sqrt(mean(z**2)). No normalization of individual embeddings, covariance estimate, model update, thresholding, or causal diagnosis occurs. A single reference sample is valid with zero variance. Comparing different encoder versions is outside the contract.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. reference=`[[0],[2]]`, current=`[[1],[3]]`: z=`[1/√1.000001]` and score=1/√1.000001. The reference mean is 1 and current mean is 2.
2. Identical constant clouds `[[4,4]]` have zero shift and score 0. Changing one current channel to 4.001 gives z≈`[1,0]`, score≈1/√2 because the variance floor is 1e-6.

## Source and scope

[Primary source](https://arxiv.org/abs/2304.07193). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute channel means/reference variance, then standardized mean differences and RMS. O((N+M)D) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
