---
{
  "schema_version": 1,
  "problem_id": "smoothquant-equivalent-rescaling",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Apply an Equivalent Channel Rescaling",
  "summary": "Apply an Equivalent Channel Rescaling",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 20,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "model-compression",
    "2022-smoothquant"
  ],
  "paper_ids": [
    "2022-smoothquant"
  ],
  "paper_sections": [
    "Selected bounded mechanism explained in theory"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; local bubblewrap baseline",
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
  "entrypoint": "solution.rescale_linear_channels",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "features/weights/scales": "dimensionless calibrated model coordinates"
    },
    "axes": "X(N,C),W(C,D),s(C,); outputs retain X and W shapes.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "X(N,C),W(C,D),s(C,); outputs retain X and W shapes."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-09,
    "atol": 1e-10,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-oracle",
      "edge-shapes",
      "invalid-contract",
      "preservation",
      "scale"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "13b00f5c6c625f0d82d8ac87e23685b193aa50680fbc3baf7f25f258503ce64f"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-021",
    "primary_urls": [
      "https://arxiv.org/abs/2211.10438"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2022-smoothquant.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root",
    "perception_completion"
  ]
}
---

# Apply an Equivalent Channel Rescaling

## Goal and contract

Implement `rescale_linear_channels(activations, weights, scales) -> (scaled_activations, scaled_weights)`. X has shape (N,C), W (C,D), scales (C,), 1<=N,C,D<=2048. Require 1e-6<=scales[j]<=1e6. Return float64 X/scales and scales[:,None]*W; output magnitudes may exceed the input bound. No quantization or calibration search occurs. Work O(NC+CD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[2,8]], W=[[3],[4]], scales=[2,4] returns [[1,2]], [[6],[16]]. Both products equal [[38]].

X=[[0,-3]], W=[[5,1],[2,-1]], scales=[1,0.5] returns [[0,-6]], [[5,1],[1,-0.5]]. Both products equal [[-6,3]].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
