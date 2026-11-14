---
{
  "schema_version": 1,
  "problem_id": "robot-data-use-risk-report",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Generate a Data-Use Risk Report",
  "summary": "Generate a Data-Use Risk Report",
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
  "entrypoint": "solution.data_use_review_flags",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "flags": "dimensionless declared-rule predicates",
      "use/embodiment IDs": "opaque request and dataset categories"
    },
    "axes": "Bounded dataset records; output sorted by dataset_id with lexical flag lists.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Bounded dataset records; output sorted by dataset_id with lexical flag lists."
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
    "evaluator_sha256": "d963e6426605337b6412c36244fd8a4a02a1dcb4808b0088daa00714c5741e3c"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-240",
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

# Generate a Data-Use Risk Report

## Contract

`data_use_review_flags(datasets, requested_use, requested_embodiment) -> list[dict]`. datasets is a list of 0..10000 exact records {dataset_id, intended_uses, prohibited_uses, embodiments, contains_personal_data, consent, license_known}; IDs unique. Each of the three lists contains 0..128 unique common IDs; both scalar requests are common IDs. contains_personal_data and license_known are bool; consent is"granted","denied" or"unknown". Both intended and prohibited may contain the same use: the request still triggers prohibited_use. Do not add a separate contradiction flag; outside_intended_use applies only when the request is absent from intended.

For each dataset emit sorted flags from: prohibited_use if request is prohibited; outside_intended_use if request is absent from intended; unsupported_embodiment if absent from embodiments; unknown_license if license_known=False; consent_denied or consent_unknown only when contains_personal_data=True and the corresponding consent value is declared. Return exact rows{dataset_id, flags, needs_review}, sorted by dataset_id, where needs_review=bool(flags). Empty flag lists mean only that these declared rules found no mismatch, not legal permission, verified consent or fitness. No policy facts are inferred from a person's identity.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

Dataset a:intended[research], prohibited[commercial], embodiments[fr3], contains_personal_data=False, consent="unknown", license_known=True. Request research/fr3 gives flags[], needs_review=False.

With personal_data=True, consent="unknown", license_known=False and request commercial/panda, flags are["consent_unknown","outside_intended_use","prohibited_use","unknown_license","unsupported_embodiment"], needs_review=True.

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
