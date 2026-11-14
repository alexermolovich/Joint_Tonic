---
{
  "schema_version": 1,
  "problem_id": "awq-activation-weighted-error",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compare Activation-Weighted Quantization Error",
  "summary": "Compare Activation-Weighted Quantization Error",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "model-compression",
    "2023-awq"
  ],
  "paper_ids": [
    "2023-awq"
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
  "entrypoint": "solution.compare_quantized_candidates",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "weight/output MSE": "dimensionless squared weight/feature units"
    },
    "axes": "X(N,C),W(C,D),candidates(K,C,D); diagnostics(K,),one chosen index.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "X(N,C),W(C,D),candidates(K,C,D); diagnostics(K,),one chosen index."
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
    "evaluator_sha256": "e1f39bba24c3cf1d6371b2f5e225f0cd4b71b8bf7fdff845e9b6e690d47d3aa5"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-095",
    "primary_urls": [
      "https://arxiv.org/abs/2306.00978"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2023-awq.md",
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

# Compare Activation-Weighted Quantization Error

## Goal and contract

Implement `compare_quantized_candidates(activations, weights, candidates) -> (weight_mse, output_mse, best_index)`. X(N,C), W(C,D), candidates(K,C,D), 1<=N,C,D<=256,1<=K<=32, K*N*C*D<=10^7. Compute float64 mean((candidate-W)^2) over C,D for each candidate, and mean((X@(candidate-W))^2) over N,D. Return both float64(K,) and Python int index of minimum output_mse; exact ties choose smallest candidate index. Use full calibration activations, including channel correlations. No mean-absolute activation proxy, scale search or weight retraining is implemented. Work O(KNCD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[10,1]], W=[[0],[0]], candidates=[[[1],[0]],[[0],[2]]] gives weight_mse=[0.5,2], output_mse=[100,4], best_index=1.

X=[[1,1]], W=[[0],[0]], candidates=[[[1],[-1]],[[0],[0]]] gives weight_mse=[1,0], output_mse=[0,0], best_index=0.

## Source and scope

Original bounded component inspired by [2023-awq](https://arxiv.org/abs/2306.00978). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
