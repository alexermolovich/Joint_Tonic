---
{
  "schema_version": 1,
  "problem_id": "deep-compression-centroid-assignment",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Quantize Shared Weight Centroids",
  "summary": "Quantize Shared Weight Centroids",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
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
  "entrypoint": "solution.assign_weight_centroids",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "weights/centroids": "dimensionless model coordinates; indices dimensionless identities"
    },
    "axes": "weights/active/indices/reconstructed(N,),centroids(K,); codebook order retained.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "weights/active/indices/reconstructed(N,),centroids(K,); codebook order retained."
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
    "evaluator_sha256": "3db7d52d425d88366d631ac383448002289717e9c227e93a34fcb219f81bf481"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-316",
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

# Quantize Shared Weight Centroids

## Goal and contract

Implement `assign_weight_centroids(weights, active, centroids) -> (indices, reconstructed)`. weights(N,),active Boolean(N,),0<=N<=100000; centroids(K,),1<=K<=256; N*K<=10^7. All weights, including inactive entries, must satisfy numeric validation. For each active entry choose the centroid minimizing absolute distance; ties choose the smallest supplied centroid index, even if centroids are unsorted or duplicated. Inactive indices=-1 and reconstructed=0. Return int64 indices(N,) and float64 reconstructed(N,). No codebook learning or centroid update occurs. Work O(NK).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

weights=[-1,0,3], active=[True,True,False], centroids=[-2,2] gives indices=[0,0,-1], reconstructed=[-2,-2,0]. Zero is tied and chooses index0.

weights=[1,4], active=[True,True], centroids=[3,1,1] gives indices=[1,0], reconstructed=[1,3].

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
