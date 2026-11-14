---
{
  "schema_version": 1,
  "problem_id": "version-simulation-distribution",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Version a Simulation Scenario Distribution",
  "summary": "Version a Simulation Scenario Distribution",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2017-domain-randomization"
  ],
  "paper_ids": [
    "2017-domain-randomization"
  ],
  "paper_sections": [
    "Mechanism described in theory; bounded teaching contract"
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
  "entrypoint": "solution.version_scenario_distribution",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "kg": "kilograms",
      "rad": "radians",
      "s": "seconds",
      "ratio": "dimensionless ratio",
      "seed": "unsigned32 integer"
    },
    "axes": "Named independent factors; every scalar uses its declared unit; episode-level reset",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "Named independent factors; every scalar uses its declared unit; episode-level reset"
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
    "evaluator_sha256": "a1962812d9b91839111938547120adf1312fc256611d4bd779d51958009222e5",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1703.06907"
    ],
    "paper_card": "research/papers/mlops-sim2real/2017-domain-randomization.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Version a Simulation Scenario Distribution

Implement version_scenario_distribution(config) -> dict.

config is an exact Python dict with keys simulator, asset_sha256, seed, reset, factors. simulator is ASCII[a-z][a-z0-9_.-]{0,63}; asset_sha256 is64 lowercase hex; seed is a built-in int0..2**32-1 excluding bool; reset must equal "episode". factors is a list of1..32 exact dicts {name,unit,low,high}. Names are unique ASCII[a-z][a-z0-9_-]{0,63}. Unit is one of kg, rad, s, ratio. low/high are built-in finite non-bool int/float with -1e6<=low<=high<=1e6; kg must have low>0, s and ratio low>=0; rad is bounded to[-pi,pi].

Normalize by sorting factors by name, converting low/high to Python float, replacing either signed zero by +0.0, and retaining all other fields. Return {"config":normalized independent dict,"sha256":digest}. Digest is SHA-256 of json.dumps(normalized,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("utf-8"). Preserve input and raise ValueError for every invalid schema/type/range.

Every factor describes an independent uniform distribution (a fixed value when low=high), sampled once per episode. Units are explicit; rad is a caller-named angular parameter, not an inferred rotation frame. This versions declarations and asset identity; it does not sample, open a simulator, check asset bytes, establish statistical equivalence of simulator versions, or prove safety.
