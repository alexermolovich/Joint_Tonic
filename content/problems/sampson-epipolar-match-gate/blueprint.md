---
{
  "schema_version": 1,
  "problem_id": "sampson-epipolar-match-gate",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Filter Geometrically Inconsistent Matches",
  "summary": "Reject correspondences inconsistent with a supplied fundamental matrix using a first-order Sampson error.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "loftr"
  ],
  "paper_ids": [
    "2021-loftr"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2021-loftr"
  ],
  "prerequisite_problem_ids": [
    "local-window-match-expectation"
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
  "entrypoint": "solution.epipolar_gate",
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
    "evaluator_sha256": "82ad25690ee83c549abada473ddc1a5a765aca877ca6b0d813d8c027c1b0151b"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2104.00680"
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

# Filter Geometrically Inconsistent Matches

Implement `epipolar_gate(source, target, fundamental, valid, threshold)`.

Reject correspondences inconsistent with a supplied fundamental matrix using a first-order Sampson error.

`source (N,2)` and `target (N,2)` are float64 matched `(x,y)` image pixels, `0<=N<=16384`. `fundamental` is a nonzero float64 `(3,3)` matrix mapping source homogeneous pixels to target epipolar lines. Normalize it by its Frobenius norm, using a max-absolute-value rescaling first to avoid underflow for tiny nonzero matrices. On the normalized matrix require second singular value >1e-8 and third singular value <=1e-8. This is the explicit numerical rank-two policy; do not project or repair the matrix. `valid` is bool `(N,)`; `threshold` is a Python int/float in `[0,100]` pixels.

For homogeneous source a=[x,y,1] and target b=[u,v,1], compute e=b.T@F@a and d=(F@a)[0]^2+(F@a)[1]^2+(F.T@b)[0]^2+(F.T@b)[1]^2. A pair is supported only if its mask is True and d is strictly greater than 1e-12. Return float64 `squared_error (N,)` equal to e squared / d for supported pairs, +Inf otherwise, and bool `accepted (N,)` for supported errors <=threshold squared. Threshold equality is accepted.

Matrix scale and sign must not affect the result, including very small nonzero scaling. Every input remains numerically validated even when its mask is False. This is an approximate epipolar diagnostic, not exact reprojection distance, robust matrix fitting, RANSAC or a guarantee that retained pairs come from a static scene.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. F=`[[0.,0.,0.],[0.,0.,-1.],[0.,1.,0.]]`, source `[[0.,0.]]`, target `[[3.,2.]]`: squared Sampson error is 2 square pixels. Threshold sqrt(2) accepts the pair; threshold 1 rejects it.
2. Change the target to `[[3.,0.]]`: the epipolar residual and squared error are zero, so threshold 0 accepts. With valid=False, squared_error is +Inf and the pair is rejected despite zero residual.

## Source and scope

[Primary source](https://arxiv.org/abs/2104.00680). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Rescale F safely, check the declared rank policy, then form both epipolar-line batches and their sensitivity denominators. O(N) arithmetic and memory beyond the fixed 3x3 SVD. Mask unsupported denominators before division.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
