---
{
  "schema_version": 1,
  "problem_id": "deep-compression-pruning-mask",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Apply a Weight-Pruning Mask",
  "summary": "Apply a Weight-Pruning Mask",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 20,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "model-compression",
    "2015-deep-compression"
  ],
  "paper_ids": [
    "2015-deep-compression"
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
  "entrypoint": "solution.prune_weights",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "weights/threshold": "dimensionless model coordinates"
    },
    "axes": "weights/mask/pruned(R,C), unchanged row-column order.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "weights/mask/pruned(R,C), unchanged row-column order."
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
    "evaluator_sha256": "5dbf2b56471d4b75d76d7db4494b03943141bc470d0433b6979449e02b8db3e2"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-020",
    "primary_urls": [
      "https://arxiv.org/abs/1510.00149"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2015-deep-compression.md",
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

# Apply a Weight-Pruning Mask

## Goal and contract

Implement `prune_weights(weights, threshold) -> (mask, pruned)`. Weights shape(R,C),1<=R,C<=2048, threshold real[0,1e6]. mask=abs(weights)>=threshold, Boolean; pruned=float64 weights where mask is true and zero otherwise. Equality is retained. At threshold zero even exact zero weights have mask=True. This computes a fixed magnitude mask; no retraining occurs. Work O(RC).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

weights=[[-0.5,0.2],[0,1]], threshold=0.5 returns mask=[[True,False],[False,True]], pruned=[[-0.5,0],[0,1]].

weights=[[0,-1]], threshold=0 returns mask=[[True,True]], pruned=[[0,-1]].

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
