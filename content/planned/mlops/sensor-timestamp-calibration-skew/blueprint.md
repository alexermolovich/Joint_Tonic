---
{
  "schema_version": 1,
  "problem_id": "sensor-timestamp-calibration-skew",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Detect Sensor Timestamp and Calibration Skew",
  "summary": "Compare aligned sensor metadata snapshots and expose timing and calibration mismatches with exact integer arithmetic.",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "sensor-timing",
    "calibration-provenance"
  ],
  "paper_ids": [
    "2019-data-validation-for-ml"
  ],
  "paper_sections": [
    "Training-serving skew checks, adapted to explicitly declared sensor metadata"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {},
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; this draft has not run"
  },
  "entrypoint": "solution.sensor_metadata_skew",
  "physical_contract": {
    "frames": [
      "Calibration IDs identify upstream frame/transform bundles"
    ],
    "units": {
      "timestamp_ns": "integer nanoseconds on one synchronized clock",
      "max_delta_ns": "nonnegative nanoseconds"
    },
    "axes": "Sensor names map corresponding streams; no vector arithmetic.",
    "timestamp_assumptions": "Snapshots describe intended paired observations; clock offset estimation is outside scope.",
    "batching": "One expected and one observed sensor map."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "time and calibration mismatch",
      "missing and unexpected sensors"
    ],
    "hidden_case_families": [
      "exact bound",
      "both reasons on one sensor",
      "zero tolerance",
      "large origins",
      "empty snapshots",
      "invalid IDs and times",
      "nonmutation"
    ],
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch3-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "The source motivates detecting mismatched data contracts. Timestamp/calibration comparison and the reason codes are original robotics extensions. Matching IDs do not verify the calibration's physical accuracy.",
    "primary_urls": [
      "https://research.google/pubs/data-validation-for-machine-learning/"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2019-data-validation-for-ml.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": ["perception_implementation"]
}
---

# Detect Sensor Timestamp and Calibration Skew

## Learning objective

Compare aligned sensor metadata snapshots and expose timing and calibration mismatches with exact integer arithmetic.

## Source and scope

The source motivates detecting mismatched data contracts. Timestamp/calibration comparison and the reason codes are original robotics extensions. Matching IDs do not verify the calibration's physical accuracy. Source location: Training-serving skew checks, adapted to explicitly declared sensor metadata. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate maps, compare name sets, evaluate two independent predicates for common sensors, sort reasons. O(S log S) time and O(S) output.

## Evaluator plan

Public cases: time and calibration mismatch; missing and unexpected sensors. Hidden cases: exact bound; both reasons on one sensor; zero tolerance; large origins; empty snapshots; invalid IDs and times; nonmutation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
