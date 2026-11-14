---
{
  "schema_version": 1,
  "problem_id": "homography-descriptor-targets",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build Homography-Supervised Descriptor Correspondence Targets",
  "summary": "Create geometric correspondence labels for descriptor-grid centers using a known homography.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "superpoint"
  ],
  "paper_ids": [
    "2017-superpoint"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-superpoint"
  ],
  "prerequisite_problem_ids": [
    "homographic-keypoint-adaptation"
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
  "entrypoint": "solution.descriptor_targets",
  "physical_contract": {
    "frames": [
      "Image pixel coordinates x right, y down; feature channels dimensionless"
    ],
    "units": {
      "values": "Pixels for geometry, dimensionless confidence and descriptors"
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
    "evaluator_sha256": "2651b304e261f138225b6d6a1fdea41784efe2265d2b7d9f073584d1e4670ca4"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1712.07629"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Build Homography-Supervised Descriptor Correspondence Targets

Implement `descriptor_targets(source_centers, target_centers, target_from_source, source_valid, target_valid, tolerance)`.

Create geometric correspondence labels for descriptor-grid centers using a known homography.

`source_centers (N,2)` and `target_centers (M,2)` are float64, `0<=N,M<=512`. They are already expressed in full-resolution `(x,y)` pixels; no stride conversion is implicit. `source_valid (N,)` and `target_valid (M,)` are bool masks. `target_from_source (3,3)` is float64 with absolute entries <=1000 and absolute determinant >=1e-9. It maps source homogeneous pixels into target pixels without automatic scale normalization. `tolerance` is a Python int/float in `[0,100]` target-image pixels.

A projected source is supported only when its absolute homogeneous denominator is strictly >1e-9. A pair is supported if both masks and this projection test pass. Return a dictionary with float64 `distances (N,M)`, Euclidean target-pixel distance for supported pairs and NaN otherwise, and bool `correspondence (N,M)`, True exactly for supported distances <=tolerance. Image bounds are not supplied: masks define valid grid centers. This isolates homography-based labels with a selectable tolerance; it does not implement the descriptor hinge loss or complete training procedure.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity warp, source centers `[[0.,0.],[2.,0.]]`, target centers `[[0.,0.],[1.,0.]]`, all valid, tolerance 1: distances `[[0.,1.],[2.,1.]]`, labels `[[True,True],[False,True]]`.
2. With the first source marked invalid, its entire distance row is NaN and its labels are False. The second row is unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Transform source centers once, then broadcast pairwise differences in target pixels. Combine masks before emitting labels and replace unsupported distances with NaN. O(NM) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
