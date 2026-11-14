---
{
  "schema_version": 1,
  "problem_id": "randomization-safety-bounds",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Choose Randomization Bounds from Safety Constraints",
  "summary": "Choose Randomization Bounds from Safety Constraints",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2018-dynamics-randomization"
  ],
  "paper_ids": [
    "2018-dynamics-randomization"
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
  "entrypoint": "solution.constrain_randomization_bounds",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "values": "caller-declared physical unit per dimension",
      "margins": "same physical unit as that dimension"
    },
    "axes": "D independent dimensions; bounds(D,2) lower then upper; no coupled safety proof",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "D independent dimensions; bounds(D,2) lower then upper; no coupled safety proof"
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
    "evaluator_sha256": "2eb20f03c573d61ccdcee7d6a3dd8951556183889828cc116f5d06bb4ceb64e3",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1710.06537"
    ],
    "paper_card": "research/papers/mlops-sim2real/2018-dynamics-randomization.md",
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

# Choose Randomization Bounds from Safety Constraints

Implement constrain_randomization_bounds(nominal, requested, allowed, margins) -> dict.

nominal is NumPy float64(D,), requested and allowed float64(D,2), margins float64(D,),1<=D<=64. All values finite with absolute value<=1e6; margins>=0. Both input intervals have low<=high. Within dimension j all values use one caller-declared physical unit; different dimensions may use different units. Requested intervals and allowed intervals are absolute parameter values, not offsets. Shrink the allowed interval to[allowed_low+margins,allowed_high-margins], then intersect with requested to obtain lo=max(requested_low,shrunk_low), hi=min(requested_high,shrunk_high).

Return feasible:bool(D,), bounds:float64(D,2), failed_dimensions:int64(F,). A dimension is feasible iff lo<=hi AND lo<=nominal[j]<=hi; endpoints inclusive and zero-width intersections allowed. Bounds contain[lo,hi] only when feasible, otherwise[NaN,NaN]. failed_dimensions is sorted ascending input indices. Preserve inputs and return independent storage; noncontiguous input valid. Invalid contracts raise ValueError.

The allowed box and margins are supplied external constraints. This only checks independent interval feasibility and nominal inclusion. It cannot prove joint dynamic safety, simulator stability, collision freedom or hardware readiness; an infeasible box is a result, not an input error.
