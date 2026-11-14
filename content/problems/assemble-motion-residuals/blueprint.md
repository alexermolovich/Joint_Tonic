---
{
  "schema_version": 1,
  "problem_id": "assemble-motion-residuals",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Assemble Obstacle and Prior Residuals",
  "summary": "Assemble a least-squares vector from an already whitened motion prior and obstacle clearance samples.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "gaussian-process-motion-planning"
  ],
  "paper_ids": [
    "2017-gaussian-process-motion-planning"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-gaussian-process-motion-planning"
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
  "entrypoint": "solution.assemble_residuals",
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
    "evaluator_sha256": "6cd6a883e8cfd1b2e78325bd121af57e4d0f549999d5180e950fa2d73328724e"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1707.07383"
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

# Assemble Obstacle and Prior Residuals

Implement `assemble_residuals(prior, clearances, margin, obstacle_sigma)`.

Assemble a least-squares vector from an already whitened motion prior and obstacle clearance samples.

`prior` is float64 `(P,)`, `0<=P<=65536`, dimensionless and already whitened. `clearances` is float64 `(N,)`, `0<=N<=65536`, signed surface-to-surface distances in meters in one fixed world; positive values mean separation. `margin` is a Python int/float in `[0,100]` meters. `obstacle_sigma` is a Python int/float in `[1e-6,1e6]` meters.

Compute obstacle residual `h=max(margin-clearances,0)/obstacle_sigma`. Return fresh float64 `residual (P+N,)` containing prior then h, and Python floats `prior_cost=0.5*sum(prior**2)`, `obstacle_cost=0.5*sum(h**2)`, `total_cost=prior_cost+obstacle_cost`, in a dictionary. Both empty arrays are allowed and give zero costs. Every supplied clearance is an observation; there is no missing-data mask. No robot geometry, distance field, prior whitening or derivative is inferred. The obstacle factor uses one independent isotropic weight; this is residual assembly, not trajectory optimization.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Prior `[2.]`, clearances `[0.1,0.5]`, margin `0.3`, sigma `0.2` give residual `[2.,1.,0.]`, prior cost `2`, obstacle cost `0.5`, total `2.5`.
2. Empty prior, clearance `[-0.1]`, margin `0`, sigma `0.1` give residual `[1.]` and total cost `0.5`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute the hinge, divide by sigma once, concatenate in the required order, and retain the separate costs for diagnostics. O(P+N) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
