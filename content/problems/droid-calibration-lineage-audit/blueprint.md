---
{
  "schema_version": 1,
  "problem_id": "droid-calibration-lineage-audit",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Audit Data and Calibration Lineage",
  "summary": "Audit Data and Calibration Lineage",
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
  "entrypoint": "solution.audit_calibration_lineage",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "timestamps": "integer nanoseconds on one synchronized clock",
      "digests": "opaque content identities"
    },
    "axes": "Episode and calibration record lists keyed by distinct IDs; sorted (episode_id,issue) results.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Episode and calibration record lists keyed by distinct IDs; sorted (episode_id,issue) results."
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
    "evaluator_sha256": "0f559783847ede734bd048e553a691626be814e16f1e7aa0bb0fe29d28299dc9"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-039",
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
    "root"
  ]
}
---

# Audit Data and Calibration Lineage

## Contract

`audit_calibration_lineage(episodes, calibrations) -> list[tuple[str, str]]`. Both are Python lists with 0..10000 records and unique IDs within each list. Episode exact fields: episode_id, session_id, robot_id, calibration_id, calibration_sha256, start_ns, end_ns. Calibration exact fields: calibration_id, session_id, robot_id, sha256, valid_from_ns, valid_until_ns. All timestamps are built-in ints in 0..2^63-1; require start<end and valid_from<valid_until. Intervals are half-open on one synchronized clock; no timezone/offset inference. Validate all supplied records even when unused.

For each episode with unknown calibration ID return only(episode_id,"unknown_calibration"). Otherwise independently emit session_mismatch, robot_mismatch, digest_mismatch, validity_gap when identities differ or the episode interval is not wholly contained in the calibration validity interval. Equality at both contained boundaries passes. Return unique tuples sorted lexicographically. Multiple declared calibration records may overlap because episode IDs select one explicitly. Digest equality compares supplied commitments; no transform or actual byte content is verified. Work O(E+C) plus issue sorting.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

Calibration k(session s, robot r, hash"1"*64, valid[0,10)) and episode a(s, r, k, samehash,[0,10)) yields[].

The same calibration with episode b(session other, robot r, k, hash"2"*64,[9,11)) yields[(b,"digest_mismatch"),(b,"session_mismatch"),(b,"validity_gap")].

## Source and scope

Original bounded component inspired by [2024-droid](https://arxiv.org/abs/2403.12945). It does not reproduce the full paper or establish hardware safety or data-use authorization.
