---
{
  "schema_version": 1,
  "problem_id": "awq-groupwise-quantization",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute Group-Wise Quantization Parameters",
  "summary": "Compute Group-Wise Quantization Parameters",
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
  "entrypoint": "solution.groupwise_quantize_weights",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "weights/scales": "dimensionless model coordinates; codes logical unsigned b-bit values"
    },
    "axes": "weights(R,C),groups(R,G,g),scales/zeros(R,G),quantized/reconstructed(R,C).",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "weights(R,C),groups(R,G,g),scales/zeros(R,G),quantized/reconstructed(R,C)."
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
    "evaluator_sha256": "cf8d945cf720e91e2bfc9daa51bf1446a10dfb1d80aadb14c1a6a6b29a4797de"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-134",
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

# Compute Group-Wise Quantization Parameters

## Goal and contract

Implement `groupwise_quantize_weights(weights, group_size, bits) -> (scales, zero_points, quantized, reconstructed)`. Weights shape(R,C),1<=R,C<=1024; group_size built-in int1..C dividing C; bits built-in int2..8. Groups are contiguous input columns within each row, G=C/group_size. For each group include zero in its range: lo=min(group_min,0), hi=max(group_max,0); Q=2**bits-1; scale=max((hi-lo)/Q, np.finfo(np.float64).tiny), or1 if hi=lo=0. The positive floor prevents underflow for subnormal input ranges. zero_point=clip(rint(-lo/scale),0,Q). q=clip(rint(weight/scale)+zero_point,0,Q), ties-to-even. Return float64 scales(R,G), int64 zero_points(R,G), uint8 quantized(R,C), float64 reconstructed=(q-zero_point)*scale. This affine reference recipe explicitly includes zero; it is not a claim to duplicate the released AWQ kernel's exact packing or group calibration. Work O(RC).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

weights=[[-1,1,0,3]], group_size=2,bits=2 gives scales=[[2/3,1]], zero_points=[[2,0]], quantized=[[0,3,0,3]], reconstructed=[[-4/3,2/3,0,3]]. Halfway rounding of -1/(2/3)=-1.5 uses -2 before adding zero point.

weights=[[0,0]], group_size=2,bits=4 gives scales=[[1]], zero_points=[[0]], quantized=[[0,0]], reconstructed=[[0,0]].

## Source and scope

Original bounded component inspired by [2023-awq](https://arxiv.org/abs/2306.00978). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
