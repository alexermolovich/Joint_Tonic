---
{
  "schema_version": 1,
  "problem_id": "egocentric-activity-confusion-report",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Aggregate Evaluation by Activity Slice",
  "summary": "An overall activity accuracy can hide a class with almost no labeled examples.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2021-ego4d"
  ],
  "paper_ids": [
    "2021-ego4d",
    "2023-ego-exo4d"
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
  "entrypoint": "solution.activity_confusion_report",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "confusion/support": "observed labeled-sample counts",
      "recall/macro_recall": "dimensionless rates",
      "labels": "categorical class indices"
    },
    "axes": "Input vectors(N,); confusion(M,C,C) axes dataset,true,predicted; recall/support(M,C).",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Input vectors(N,); confusion(M,C,C) axes dataset,true,predicted; recall/support(M,C)."
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
    "evaluator_sha256": "a847a465fdb9e0a5142bf99b427ec8f5d98f0b5a9d4ba2bc34b8c441a803d462"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-003",
    "primary_urls": [
      "https://arxiv.org/abs/2110.07058"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2021-ego4d.md",
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

# Aggregate Evaluation by Activity Slice

## Contract

activity_confusion_report(dataset_ids,truth,prediction,observed,num_classes) -> dict{dataset_ids,confusion,support,recall,macro_recall}. dataset_ids int64(N,) nonnegative,truth/prediction int64(N,),observed bool(N,),0<=N<=100000,num_classes built-in int1..64. For observed rows both labels must in[0,C); unobserved label placeholders may be arbitrary int64 and are ignored. Include all sorted dataset IDs, even with no observed labels. Return confusion int64(M,C,C) with axes(dataset,true,predicted), support int64(M,C) row sums,recall float64(M,C)=diagonal/support with NaN missing true classes; macro_recall float64(M,) mean only over supported true classes or NaN. Require M*C*C<=1e6. Predictions on absent true classes still count as columns for measured rows. This is a bounded classification diagnostic, not official Ego4D/Ego-Exo4D metrics for every task or robot-action supervision.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

dataset[0,0,0],truth[0,0,1],prediction[0,1,0],observed allTrue,C2 -> confusion[[[1,1],[1,0]]],support[[2,1]],recall[[.5,0]],macro[.25].

### Example 2

dataset[2,2],truth[-1,1],prediction[99,1],observed[False,True],C3 -> support[[0,1,0]],recall[[NaN,1,NaN]],macro[1].

## Source and scope

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). It does not reproduce the full dataset loader, task suite or headline results.
