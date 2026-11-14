---
{
  "schema_version": 1,
  "problem_id": "oxe-version-dataset-manifest",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Version a Cross-Robot Dataset Manifest",
  "summary": "A mixed dataset needs an identity that includes its versions, embodiments and calibration.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-open-x-embodiment",
    "policy-components"
  ],
  "paper_ids": [
    "2023-open-x-embodiment"
  ],
  "paper_sections": [
    "Original lineage exercise motivated by cross-robot dataset reproducibility. Hashes are caller-supplied commitments, not proof that actual remote bytes match them."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
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
  "entrypoint": "solution.version_dataset_manifest",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Registry IDs, semantic versions and byte-content hashes have no physical units; calibration hashes identify externally pinned physical conventions."
    },
    "axes": "bounded record list -> canonical JSON string and SHA256 string",
    "timestamp_assumptions": "An immutable snapshot, not a mutable latest-version pointer; no wall clock enters the digest.",
    "batching": "bounded record list -> canonical JSON string and SHA256 string"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original lineage exercise motivated by cross-robot dataset reproducibility. Hashes are caller-supplied commitments, not proof that actual remote bytes match them.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "paper_card": "research/papers/vla-embodied/2023-open-x-embodiment.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Version a Cross-Robot Dataset Manifest

## Contract

`version_dataset_manifest(datasets,schema_version)` takes a Python list of0..128 records and a built-in integer schema_version1..1000, excluding bool. Each record is a dict with exactly dataset_id, version, embodiment, content_sha256, calibration_sha256. dataset_id and embodiment match [A-Za-z][A-Za-z0-9_-]{0,31}; version matches nonnegative decimal major.minor.patch with no leading zeros except0, each component<=9999; hashes are64 lowercase hexadecimal characters. IDs must be unique. Sort records by dataset_id, construct payload={"schema_version":schema_version,"datasets":sorted_records}, and serialize with json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=True). Return {"canonical_json":str,"sha256":lowercase SHA256 of its UTF-8 bytes}. Input dict/list order must not change the digest; any content/calibration/version change must. Do not read external files or fetch URLs.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original lineage exercise motivated by cross-robot dataset reproducibility. Hashes are caller-supplied commitments, not proof that actual remote bytes match them.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
