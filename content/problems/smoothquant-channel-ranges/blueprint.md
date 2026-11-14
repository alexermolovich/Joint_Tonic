---
{
  "schema_version": 1,
  "problem_id": "smoothquant-channel-ranges",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Measure Per-Channel Activation and Weight Ranges",
  "summary": "Measure Per-Channel Activation and Weight Ranges",
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
  "entrypoint": "solution.calibration_channel_ranges",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "features/weights/ranges": "dimensionless calibrated model coordinates"
    },
    "axes": "X(N,C),W(C,D); two channel vectors(C,).",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "X(N,C),W(C,D); two channel vectors(C,)."
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
    "evaluator_sha256": "e1242823c72ee424e2f6d49806ccd1d34007ae8d414b5dc784eb9f573f2d283a"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-276",
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

# Measure Per-Channel Activation and Weight Ranges

## Goal and contract

Implement `calibration_channel_ranges(activations, weights) -> (activation_max, weight_max)`. Activations have shape (N,C), weights (C,D), with 1<=N,C,D<=2048. Return two float64 arrays (C,): maximum absolute calibration activation over N, and maximum absolute weight over D. A completely zero channel has maximum zero. Empty axes are invalid. Work O(NC+CD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[1,-4],[3,2]], W=[[2,-1],[0,-5]] gives activation_max=[3,4], weight_max=[2,5].

X=[[0,2]], W=[[0],[3]] gives activation_max=[0,2], weight_max=[0,3].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
