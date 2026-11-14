---
{
  "schema_version": 1,
  "problem_id": "droid-scene-collector-split",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Split Demonstrations by Scene and Collector",
  "summary": "Split Demonstrations by Scene and Collector",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2024-droid"
  ],
  "paper_ids": [
    "2024-droid"
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
  "entrypoint": "solution.split_scene_collector_components",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "episode/scene/collector IDs": "opaque collection identities"
    },
    "axes": "One episode record per unique ID; scene and collector namespaces are distinct; output IDs sorted.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "One episode record per unique ID; scene and collector namespaces are distinct; output IDs sorted."
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
    "evaluator_sha256": "43205cee4368cd939e1e48cc6aaec2feb2d1e518d8a3941737416d68db2a91e8"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-383",
    "primary_urls": [
      "https://arxiv.org/abs/2403.12945"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2024-droid.md",
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

# Split Demonstrations by Scene and Collector

## Contract

`split_scene_collector_components(episodes, held_out_scenes) -> dict`. episodes is a list of 0..10000 exact {episode_id, scene_id, collector_id} records with unique episode IDs; held_out_scenes is a list of 0..10000 unique declared scene IDs. Empty episodes require empty held-out scenes. Join episodes sharing a scene OR a collector; take the transitive closure. A component goes to test if any episode in it has a held-out scene; all other components go to train. Return train_ids and test_ids sorted lists plus component_ids mapping every episode_id to the lexically smallest episode_id in its connected component. This is deterministic group isolation, not a random proportional split or the dataset's published benchmark split. Work near-linear union/find plus sorting; preserve inputs.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

episodes a(s1, c1), b(s2, c1), c(s2, c2), d(s3, c3), held_out_scenes=[s1] gives test_ids[a, b, c], train_ids[d], component_ids{a:a, b:a, c:a, d:d}. Collector and scene links propagate transitively.

For a(s1, c1), b(s2, c2) and held_out_scenes=[], train_ids=[a, b], test_ids=[], component_ids{a:a, b:b}.

## Source and scope

Original bounded component inspired by [2024-droid](https://arxiv.org/abs/2403.12945). It does not reproduce the full paper or establish hardware safety or data-use authorization.
