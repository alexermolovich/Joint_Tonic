---
{
  "schema_version": 1,
  "problem_id": "smoothquant-layer-error-report",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Validate Layer Output Error After Smoothing",
  "summary": "Validate Layer Output Error After Smoothing",
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
  "entrypoint": "solution.layer_error_report",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "error/tolerance": "dimensionless feature units; RMSE/max preserve units, relativeL2 unitless"
    },
    "axes": "reference/candidate(N,D); row diagnostics(N,); one aggregate relative scalar.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "reference/candidate(N,D); row diagnostics(N,); one aggregate relative scalar."
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
    "evaluator_sha256": "60ffa47d68ba7442343d1a9c89a01b0a6030be240b99d40e905ef564b883bb6e"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-432",
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

# Validate Layer Output Error After Smoothing

## Goal and contract

Implement `layer_error_report(reference, candidate, absolute_tolerance) -> dict`. Both arrays shape(N,D),1<=N,D<=2048; tolerance real in[0,1e6]. Return float64 row_rmse(N,), row_max_abs(N,), bool failed_rows(N,), Python float relative_l2, and Python bool passed. Let error=candidate-reference; row_rmse=sqrt(mean(error^2,axis=1)); failed_rows=row_max_abs>tolerance. relative_l2=norm(error)/max(norm(reference),1e-12), with Frobenius norms over all entries. passed means no failed row. Equality to tolerance passes. This gate has absolute per-output units; relative_l2 is a diagnostic only. Work O(ND).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

reference=[[3,4],[0,0]], candidate=[[3,5],[0,0]], tolerance=1 gives row_rmse=[sqrt(0.5),0], row_max_abs=[1,0], failed_rows=[False,False], relative_l2=0.2, passed=True.

reference=[[0]], candidate=[[2]], tolerance=1 gives row_rmse=[2], row_max_abs=[2], failed_rows=[True], relative_l2=2e12, passed=False.

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
