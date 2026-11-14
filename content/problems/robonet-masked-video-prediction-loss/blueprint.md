---
{
  "schema_version": 1,
  "problem_id": "robonet-masked-video-prediction-loss",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute a Masked Video-Prediction Loss",
  "summary": "A padded video frame is not a black target.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2019-robonet"
  ],
  "paper_ids": [
    "2019-robonet"
  ],
  "paper_sections": [
    "Mechanism explicitly scoped in the contract"
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
  "entrypoint": "solution.masked_video_loss",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "pixel values": "dimensionless normalized intensities",
      "loss/per_horizon": "mean squared normalized-pixel residual",
      "frame_counts": "observed frame counts"
    },
    "axes": "Prediction/target(B,T,H,W,C),valid(B,T),per-horizon outputs(T,).",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Prediction/target(B,T,H,W,C),valid(B,T),per-horizon outputs(T,)."
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
    "evaluator_sha256": "24bba0d15cece79f5cb7225da46dd6017463113158041cdd05e31f79dc061fcb"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-119",
    "primary_urls": [
      "https://arxiv.org/abs/1910.11215"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2019-robonet.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Compute a Masked Video-Prediction Loss

## Contract

masked_video_loss(predicted,target,valid) -> dict{loss,per_horizon,frame_counts,has_data}. predicted/target float(B,T,H,W,C) same shape,0<=B<=256,1<=T<=256,1<=H,W<=64,C in{1,3},total entries<=1e6. valid bool(B,T). At valid frames all pixels must finite[0,1]; invalid frames may contain arbitrary finite/NaN/Inf placeholders and are completely ignored. Per-frame MSE averages ALL HWC pixel/channel squared differences; loss averages over all valid frames, not equally over horizons. per_horizon float64(T,) averages valid frames at each horizon, NaN when none; frame_counts int64(T,); has_data Python bool. If no data, loss0,has_dataFalse,all per_horizonNaN. This simple normalized-pixel regression is an original bounded teaching objective, not all RoboNet model losses or a perceptual quality score.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

B1,T2,H1,W2,C1: target valid firstframe[0,1],prediction[.2,.8],secondframe padded; valid[[True,False]] -> loss.04,per_horizon[.04,NaN],counts[1,0],has_dataTrue.

### Example 2

B2,T2,one-pixel target0; prediction[[0,1],[1,NaN]],valid[[True,True],[True,False]] -> loss2/3,per_horizon[.5,1],counts[2,1].

## Source and scope

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). It does not reproduce the full dataset loader, task suite or headline results.
