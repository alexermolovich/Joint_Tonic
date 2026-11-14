---
{
  "schema_version": 1,
  "problem_id": "rank-motion-candidates",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Rank Multi-Seed Motion Trajectories",
  "summary": "Rank supplied motion candidates after explicit feasibility gates.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "curobo"
  ],
  "paper_ids": [
    "2023-curobo"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2023-curobo"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.rank_trajectories",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "e9695fc3d5f8db1d07f26631ec14ad44b1fb3b180573af6dede6f0e3b3cf22c9"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.17274"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Rank Multi-Seed Motion Trajectories

Implement `rank_trajectories(endpoint_error, collision_free, limits_ok, objective, endpoint_tolerance)`.

Rank supplied motion candidates after explicit feasibility gates.

`endpoint_error` and `objective` are nonnegative float64 `(N,)`, `0<=N<=100000`. `collision_free` and `limits_ok` are bool `(N,)`. `endpoint_tolerance` is a Python int/float in `[0,1e6]`. Errors use one normalized endpoint-distance convention; objectives use one common normalized cost. All candidates describe the same start/goal task and validation setup.

A candidate is eligible exactly when both supplied flags are True and endpoint_error<=endpoint_tolerance. Return a dictionary with fresh bool `feasible (N,)`, int64 `order (F,)` containing only eligible indices sorted by `(objective,index)`, and Python int `best`, the first ordered index or -1 when none are eligible. Endpoint equality passes; exact cost ties keep the original index order. Empty input is valid. Flags summarize caller-performed validation, which may be sampled; they do not establish continuous collision freedom. This selection component neither optimizes trajectories nor runs cuRobo.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Errors `[0.1,0.2,0.05]`, both flags all True, objectives `[3.,1.,3.]`, tolerance `0.1` give feasible `[True,False,True]`, order `[0,2]`, best `0`.
2. Errors `[0.]`, collision flag `[False]`, limits flag `[True]`, objective `[0.]`, tolerance `0` give feasible `[False]`, empty int64 order and best `-1`.

## Source and scope

[Primary source](https://arxiv.org/abs/2310.17274). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build the Boolean eligibility mask, collect original indices in order, and use a stable sort by their objectives. O(N+F log F) time and O(N) memory, with F eligible candidates.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
