---
{
  "schema_version": 1,
  "problem_id": "pointnet-shared-mlp",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Shared Point MLP and Global Feature",
  "summary": "Apply one shared affine/ReLU layer to every point, then max-pool each feature channel.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "pointnet",
    "pointnet-shared-mlp"
  ],
  "paper_ids": [
    "2017-pointnet"
  ],
  "paper_sections": [
    "Network architecture: shared per-point mapping and symmetric aggregation; original input-data diagnostics"
  ],
  "track_ids": [
    "paper-2017-pointnet"
  ],
  "prerequisite_problem_ids": [
    "pointnet-symmetric-pooling"
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
  "entrypoint": "solution.point_mlp",
  "physical_contract": {
    "frames": [
      "Declared sensor or feature frame"
    ],
    "units": {
      "values": "Defined in the contract"
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
    "evaluator_sha256": "754569e257e77e9ddefcfa7b7083fda6d7b9e7a58e4546b9d537de2ea6f0c817"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1612.00593"
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

# Build a Shared Point MLP and Global Feature

Implement `point_mlp(points: np.ndarray, weights: np.ndarray, bias: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Apply one shared affine/ReLU layer to every point, then max-pool each feature channel.
`points` has shape (N,D), 1<=N<=4096, 1<=D<=128; `weights` (D,F), 1<=F<=128; `bias` (F,). Return `(local, global_feature)` of shape (N,F) and (F,), both float64. The formula is `local=max(points @ weights + bias,0)`; global_feature is the maximum over points, independently for each feature. Empty clouds are rejected. Features are dimensionless, already normalized upstream; columns are not assumed xyz. This is a single-layer PointNet teaching block, without the T-Net, batch normalization, or learned classifier.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. `points=[[1,2],[-1,3]], weights=I₂, bias=[0,-2]` gives local `[[1,0],[0,1]]` and global `[1,1]`.
2. A single point `[[2]]`, weight `[[-3]]`, bias `[1]` gives local `[[0]]` and global `[0]`: ReLU happens before pooling.

## Source and scope

[Primary source](https://arxiv.org/abs/1612.00593). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute the affine layer, apply ReLU, and reduce over the point axis. Time O(NDF); returned feature storage O(NF).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
