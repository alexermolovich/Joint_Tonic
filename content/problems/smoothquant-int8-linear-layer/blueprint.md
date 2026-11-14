---
{
  "schema_version": 1,
  "problem_id": "smoothquant-int8-linear-layer",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Quantize Weights and Activations to Int8",
  "summary": "Quantize Weights and Activations to Int8",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
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
  "entrypoint": "solution.quantize_int8_layer",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "scales/output": "dimensionless calibrated feature values"
    },
    "axes": "X(N,C),W(C,D),qx(N,C),qw(C,D),sx(N,1),sw(1,D),output(N,D).",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "X(N,C),W(C,D),qx(N,C),qw(C,D),sx(N,1),sw(1,D),output(N,D)."
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
    "evaluator_sha256": "cb5feb74cd23da52f92aab4fe812e60622baf7820a9475d88a3d8ec04deeb811"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-317",
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

# Quantize Weights and Activations to Int8

## Goal and contract

Implement `quantize_int8_layer(activations, weights) -> (qx, qw, sx, sw, output)`. X(N,C), W(C,D), 1<=N,C,D<=1024, N*C*D<=10^7. Use symmetric integer range [-127,127]. sx(N,1)=max(abs(X),axis=1)/127; sw(1,D)=max(abs(W),axis=0)/127. Replace a zero scale with exactly 1. Quantize with round-to-nearest ties-to-even then clip; qx/qw have dtype int8. Return scales float64 and output(N,D)=(qx.astype(int64) @ qw.astype(int64))*sx*sw in float64. This is a numerical simulation, not an optimized int8 kernel. Work O(NCD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[127,0]], W=[[1],[0]] gives qx=[[127,0]], qw=[[127],[0]], sx=[[1]], sw=[[1/127]], output=[[127]].

X=[[0,0]], W=[[0],[0]] gives zero int8 arrays, sx=[[1]], sw=[[1]], output=[[0]].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
