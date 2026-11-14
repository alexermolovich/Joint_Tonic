---
{
  "schema_version": 1,
  "problem_id": "ray-recovery-reconciliation",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Recover Failed Worker Tasks Idempotently",
  "summary": "Recover Failed Worker Tasks Idempotently",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2017-ray"
  ],
  "paper_ids": [
    "2017-ray"
  ],
  "paper_sections": [
    "Operational component discussed in Theory; explicit original teaching policy"
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
  "entrypoint": "solution.reconcile_task_attempts",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "attempt": "dimensionless attempt ordinal",
      "digest": "opaque SHA256 content identity"
    },
    "axes": "Task records keyed by task_id; unordered terminal events keyed by(task_id,attempt); lexical task output.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Task records keyed by task_id; unordered terminal events keyed by(task_id,attempt); lexical task output."
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
    "evaluator_sha256": "97abcf2eb02fce31cc7e42f13b572dde7a2866d46e4b3ac924ad2f5e3cbea4fa"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-330",
    "primary_urls": [
      "https://arxiv.org/abs/1712.05889"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2017-ray.md",
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

# Recover Failed Worker Tasks Idempotently

## Contract

`reconcile_task_attempts(tasks, events, max_attempts) -> list[dict]`. tasks is a list of 1..10000 exact {task_id, replay_safe} records with unique IDs and Boolean replay_safe. events is a list of 0..50000 exact {task_id, attempt, status, digest} records. Each task must be declared; attempt is int in 1..max_attempts; status is "failed" or "succeeded"; a failed event has digest=None, a succeeded event has a valid SHA256. max_attempts is int in 1..16. Repeated identical events are ignored; contradictory status/digest records for the same(task, attempt) raise ValueError. Multiple successful attempts for one task must agree on digest or raise ValueError. Event order has no meaning.

For each task: any success commits state "succeeded", digest agreed, next_attempt=None, regardless of later failed attempts. Without success, no observed attempts gives state "pending", next_attempt=1, even if replay_safe=False. Otherwise highest attempt==max_attempts gives state "exhausted", next_attempt=None. Otherwise replay_safe=False gives state "blocked", next_attempt=None; otherwise state "retry", next_attempt=highest+1. Non-success digest=None. Return exact {task_id, state, next_attempt, digest} rows sorted by task_id. This reconciles supplied terminal evidence, not an executor or exactly-once side-effect guarantee.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

tasks=[{task_id:"a", replay_safe:True},{task_id:"b", replay_safe:False}], events=[{task_id:"a", attempt:1, status:"failed", digest:None}], max_attempts=3 gives a:state "retry", next_attempt=2 and b:state "pending", next_attempt=1; both digest=None.

For one replay-safe task a, successful attempt 1 with digest"1"*64 plus failed attempt 2 under max_attempts=3 gives state "succeeded", next_attempt=None, digest"1"*64. Repeating either event does not change the result.

## Source and scope

Original bounded component inspired by [2017-ray](https://arxiv.org/abs/1712.05889). It does not reproduce the full paper or establish hardware safety or data-use authorization.
