---
{
  "schema_version": 1,
  "problem_id": "keypoint-repeatability",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Evaluate Keypoint Repeatability",
  "summary": "Evaluate symmetric nearest-point repeatability within the shared image region.",
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
  "entrypoint": "solution.keypoint_repeatability",
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
    "evaluator_sha256": "f15abe8c6a8cf3fa9081512b3a73318de8eb9cecf894347dcc869bc41e12d00f"
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

# Evaluate Keypoint Repeatability

Implement `keypoint_repeatability(source, target, target_from_source, source_size, target_size, threshold)`.

Evaluate symmetric nearest-point repeatability within the shared image region.

`source (N,2)` and `target (M,2)` are float64 points in their respective images, `0<=N,M<=512`. `source_size` and `target_size` are int64 `(2,)` `[height,width]`, each 1..4096; all supplied points must be inside their own closed pixel-center domain `[0,width-1] x [0,height-1]`. `target_from_source` is float64 `(3,3)`, absolute entries <=1000, absolute determinant >=1e-9, mapping source to target homogeneous pixels. Do not normalize its scale. `threshold` is a Python int/float in `[0,100]` pixels.

Project source points forward and target points with the matrix inverse. Projection is supported only for absolute denominator strictly >1e-9. A point is eligible if its projection is supported and lies inside the other image's closed center domain. Each eligible source is correct if its projected target location is within threshold (inclusive) of any eligible target. Each eligible target is correct if its inverse projection is within threshold of any eligible source, measured in source pixels.

Return bool arrays `source_eligible (N,)`, `target_eligible (M,)`, `source_correct (N,)`, `target_correct (M,)`, plus Python float `repeatability`: total correct divided by total eligible across both directions, or NaN if no points are eligible. Ineligible points are never correct. Empty opposite candidate sets have no correct points. Multiple detections may use the same nearest neighbor: this is a repeatability diagnostic, not a one-to-one assignment or a homography estimator.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity warp, source points `[[0.,0.],[2.,0.]]`, target `[[0.,0.]]`, both image sizes `[3,3]`, threshold 0: source correctness `[True,False]`, target correctness `[True]`, repeatability `2/3`.
2. The same image sizes with one point `[0.,0.]` in each image and target-from-source x translation +3 have no shared support. Both eligibility flags are False and repeatability is NaN.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Project in both directions, form overlap masks, and compare only eligible opposite points. Compute the two distance matrices separately because each uses different pixel units under a scale-changing homography. O(NM) time and O(NM) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
