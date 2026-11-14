---
{
  "schema_version": 1,
  "problem_id": "robonet-transition-frame-windows",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Align Actions and Images in a Video Window",
  "summary": "An action belongs between two frames.",
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
  "entrypoint": "solution.video_transition_windows",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "images": "dimensionless normalized pixel intensities",
      "actions": "caller-declared embodiment command units",
      "indices": "frame indices,not elapsed time"
    },
    "axes": "Source images(T,H,W,C),actions(T-1,D); outputs images(S,K,H,W,C),actions(S,K,D),valid(S,K).",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Source images(T,H,W,C),actions(T-1,D); outputs images(S,K,H,W,C),actions(S,K,D),valid(S,K)."
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
    "evaluator_sha256": "b6dbc45aeb1ed68d480b3293901dba8ecb1fe9661dfd9537fc7570954316dd0f"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-010",
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
    "research_curator",
    "perception_completion"
  ]
}
---

# Align Actions and Images in a Video Window

## Contract

video_transition_windows(images,actions,observed,episode_ids,starts,horizon) -> dict{current,next,actions,valid}. images float(T,H,W,C),1<=T<=4096,1<=H,W<=64,C in{1,3},finite[0,1]; actions float(max(T-1,0),D),1<=D<=32,finite abs<=1e4. observed bool(T,),episode_ids int64(T,) nonnegative and nondecreasing, so an episode identity never resumes after a boundary. starts int64(S,),0<=S<=4096, each0<=start<T. horizon built-in int1..256. Image input entries and total output image entries 2*S*horizon*H*W*C each<=1e6; output action entries S*horizon*D<=1e6. For each window start s and offset k, transition t=s+k is valid iff t+1<T, both frames observed AND episode_ids[t]==episode_ids[t+1]==episode_ids[s]. Valid output is images[t],images[t+1],actions[t]; invalid output allzeros and validFalse. Use images/action tensors with output shapes(S,horizon,H,W,C)/(S,horizon,D). All source values validate even when masked. The convention says a_t acts from frame t to frame t+1; it does not interpolate asynchronous sensors or infer an action coordinate frame. Actions retain caller-defined embodiment units.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

one-pixel images[0,.2,.4],actions[[1],[2]],observed allTrue,episodes[0,0,0],starts[0],horizon3 -> current[0,.2,0],next[.2,.4,0],actions[1,2,0],valid[True,True,False] (shown without singleton axes).

### Example 2

Same data with episodes[0,1,1] and start0,horizon2 -> both transitions invalid; the second transition belongs to a different episode from the window start.

## Source and scope

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). It does not reproduce the full dataset loader, task suite or headline results.
