---
{
  "schema_version": 1,
  "problem_id": "robot-dataset-datasheet-schema",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Validate a Robot Dataset Datasheet",
  "summary": "Validate a Robot Dataset Datasheet",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2018-datasheets-for-datasets"
  ],
  "paper_ids": [
    "2018-datasheets-for-datasets"
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
  "entrypoint": "solution.validate_robot_datasheet",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "fields/IDs/hashes": "qualitative documentation and opaque provenance identities"
    },
    "axes": "One bounded documentation dict; one located issue at most per present known field, plus missing/unexpected fields.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "One bounded documentation dict; one located issue at most per present known field, plus missing/unexpected fields."
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
    "evaluator_sha256": "837f348440f045514f322005109a26ccee13ef243fd2d9061d66b4435d858bb9"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-418,PB-176",
    "primary_urls": [
      "https://arxiv.org/abs/1803.09010"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2018-datasheets-for-datasets.md",
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

# Validate a Robot Dataset Datasheet

## Contract

`validate_robot_datasheet(document) -> list[tuple[str, str]]`. document must be a Python dict with at most 32 string keys (each1..64 chars); otherwise raise ValueError. Required text fields are dataset_id, version, motivation, collection_method, calibration_sha256, license, maintenance, limitations. Required list fields are embodiments, sensors, tasks, intended_uses, prohibited_uses. Extra keys each produce(key,"unexpected"). Absent required fields each produce(key,"missing").

Present text fields must be str of 1..1024 characters after strip; otherwise report invalid. Stripping is used only to check text nonemptiness and length; ID, version and digest syntax are checked on the original string with ASCII digits. dataset_id must additionally match the common ID rule; version must contain exactly three decimal integer components separated by literal dots, each component in 0..9999 and no leading zeros except0; calibration_sha256 must be a valid digest. A literal string"unknown" is permitted only for calibration_sha256 or license and produces unknown instead of invalid. Lists must be Python lists of0..128 unique common IDs; embodiments, sensors, tasks, intended_uses must be nonempty, prohibited_uses may be empty. Any malformed list yields one invalid issue at its field, not per-item issues. Return tuples sorted lexically, at most one issue per present field. Do not infer actual consent, rights or quality from completeness. This one schema task also implements missing provenance detection.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

A complete document has dataset_id="fr3_set", version="1.0.0", motivation="pick blocks", collection_method="teleoperation", calibration_sha256="1"*64, license="CC0-1.0", maintenance="lab", limitations="one room", embodiments=["fr3"], sensors=["wrist_rgb"], tasks=["pick"], intended_uses=["research"], prohibited_uses=[]. Its report is[].

Starting from that document, delete license, set calibration_sha256="unknown", and add extras=1. Report[("calibration_sha256","unknown"),("extras","unexpected"),("license","missing")].

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
