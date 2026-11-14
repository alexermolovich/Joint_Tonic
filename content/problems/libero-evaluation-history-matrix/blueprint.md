---
{
  "schema_version": 1,
  "problem_id": "libero-evaluation-history-matrix",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Record a Continual-Learning Evaluation Matrix",
  "summary": "A final score cannot show when a robot gained or lost a skill.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2023-libero"
  ],
  "paper_ids": [
    "2023-libero"
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
  "entrypoint": "solution.continual_evaluation_matrix",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "stage": "training-stage ordinal,0 is initial policy",
      "counts/successes": "distinct evaluation-trial counts",
      "rates": "dimensionless success fraction"
    },
    "axes": "Output(K+1,K): rows training stage, columns declared task order.",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Output(K+1,K): rows training stage, columns declared task order."
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
    "evaluator_sha256": "8a77fa7262521e73c4b97145a6990c4637453d8031b0778dfca0dec0874a3c03"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-327",
    "primary_urls": [
      "https://arxiv.org/abs/2306.03310"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2023-libero.md",
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

# Record a Continual-Learning Evaluation Matrix

## Contract

continual_evaluation_matrix(task_order, events) -> dict{counts,successes,rates}. task_order list1..256 unique common taskIDs. events list0..100000 exact records{evaluation_id,stage,task_id,success}; evaluation_id commonID; stage built-in int0..K where K=len(task_order), task_id must be declared, success bool. stage0 is initial policy; stage i is after learning first i tasks. A repeated identical evaluation_id record is idempotent; any conflicting field for same evaluation_id raises ValueError. Distinct IDs remain distinct trials even if other fields coincide. Return counts/successes int64(K+1,K), rates float64(K+1,K)=successes/counts with NaN at zero count. Column order is task_order; rows are learning stages including0. Observing future tasks at earlier stages is valid for forward-transfer evidence. No missing cell is imputed.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

task_order=[a,b],events e1(stage0,b,False),e2(stage1,a,True),e2 repeated -> counts[[0,1],[1,0],[0,0]],successes[[0,0],[1,0],[0,0]],rates[[NaN,0],[1,NaN],[NaN,NaN]].

### Example 2

task_order=[a], events e1(stage1,a,True),e2(stage1,a,False) -> counts[[0],[2]],successes[[0],[1]],rates[[NaN],[0.5]].

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
