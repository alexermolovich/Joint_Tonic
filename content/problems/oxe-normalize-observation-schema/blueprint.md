---
{
  "schema_version": 1,
  "problem_id": "oxe-normalize-observation-schema",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Normalize Heterogeneous Robot Observation Schemas",
  "summary": "Robot datasets often describe the same signal under different keys and units.",
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
    "Original shared-schema adapter motivated by Open X-Embodiment dataset standardization. Field mapping and scaling are explicit educational policy, not the complete OXE dataset transforms."
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
  "entrypoint": "solution.normalize_observations",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Caller supplies multiplicative conversion factors such as centimeters to meters0.01 or degrees to radianspi/180; output units are the declared canonical units."
    },
    "axes": "raw fields(T,Df), timestamps(T) -> canonical feature dict(T,Df) and timestamps(T)",
    "timestamp_assumptions": "One synchronized strictly increasing timestamp vector applies to every field; this function cannot align unsynchronized records.",
    "batching": "raw fields(T,Df), timestamps(T) -> canonical feature dict(T,Df) and timestamps(T)"
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
    "authoring_notes": "Original shared-schema adapter motivated by Open X-Embodiment dataset standardization. Field mapping and scaling are explicit educational policy, not the complete OXE dataset transforms.",
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

# Normalize Heterogeneous Robot Observation Schemas

## Contract

`normalize_observations(raw,mapping,scales,timestamps)` takes raw:dict of1..16 named real matrices(T,Df),1<=T<=4096,1<=Df<=64; timestamps(T,) strictly increasing seconds>=0; mapping:dict of1..16 canonical_name->existing raw_name; scales:dict with exactly mapping keys and positive numeric scalar factors<=1000. Every raw field, including unused fields, must share T and be valid. All names are ASCII identifiers matching [A-Za-z][A-Za-z0-9_]{0,31}. Return dict timestamps:float64(T,) and features:dict with exactly canonical names, each value = raw[source]*scale as an independent float64(T,Df) copy. Multiple canonical names may reference one source. Unknown source names and missing/extra scales are invalid. No implicit frame transform, resampling, offsets or missing-value fill.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original shared-schema adapter motivated by Open X-Embodiment dataset standardization. Field mapping and scaling are explicit educational policy, not the complete OXE dataset transforms.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
