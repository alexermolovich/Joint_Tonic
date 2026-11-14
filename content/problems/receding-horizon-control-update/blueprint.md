---
{
  "schema_version": 1,
  "problem_id": "receding-horizon-control-update",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Update a Receding-Horizon Control Sequence",
  "summary": "Apply a weighted rollout perturbation, bound the control sequence, and recede by one step.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "path-integral-mpc"
  ],
  "paper_ids": [
    "2015-path-integral-mpc"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2015-path-integral-mpc"
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
  "entrypoint": "solution.update_control_plan",
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
    "evaluator_sha256": "7d5c23c4e824916e8016b69df99bba0982610654b50cd3e53328c8ad65b0c1db"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1509.01149"
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

# Update a Receding-Horizon Control Sequence

Implement `update_control_plan(controls, perturbations, weights, lower, upper)`.

Apply a weighted rollout perturbation, bound the control sequence, and recede by one step.

`controls` float64 `(H,D)`, `1<=H<=128`, `1<=D<=16`, and `perturbations` float64 `(K,H,D)`, `1<=K<=256`, contain joint-velocity commands in radians/second for a fixed caller-declared control period. `weights` float64 `(K,)` are nonnegative and their sum must differ from1 by at most1e-9; use the supplied weights as-is without renormalizing. `lower,upper` float64 `(D,)` are command limits in radians/second, lower<=upper. Controls may start outside the limits; clipping happens after adding the weighted update. Compute `updated=clip(controls+sum_k(weights[k]*perturbations[k]),lower,upper)`. Return dict `updated`: fresh float64 `(H,D)`, `action`: fresh `(D,)` copy of updated first row, `next_plan`: fresh `(H,D)` containing updated rows1..H-1 followed by a repeat of updated's last row. H1 repeats its sole row. Outputs must not alias each other or inputs. This returns a proposed action only; it does not execute the action or step a robot. Clipping and last-row padding are explicit teaching policies, not a preservation claim for every MPPI theoretical guarantee.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Controls `[[0.],[1.]]`, perturbations `[[[2.],[0.]],[[0.],[2.]]]`, weights `[0.25,0.75]`, limits `[-1.]` to `[2.]`: updated `[[0.5],[2.]]`, action `[0.5]`, next plan `[[2.],[2.]]`.
2. One-step control `[[3.]]`, one zero perturbation, weight `[1.]`, limits `[-1.]` to `[1.]`: updated `[[1.]]`, action `[1.]`, next plan `[[1.]]`, all independent arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(KHD) time and O(KHD) input validation footprint, with O(HD) outputs. Reduce only the rollout axis, clip each command, and copy the selected action before constructing the shifted plan.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
