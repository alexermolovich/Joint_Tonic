---
{
  "schema_version": 1,
  "problem_id": "deepmimic-reference-pose",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Interpolate a Reference Motion Pose",
  "summary": "A reference motion is sampled at discrete times, while a controller may request an intermediate pose.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2018-deepmimic",
    "policy-components"
  ],
  "paper_ids": [
    "2018-deepmimic"
  ],
  "paper_sections": [
    "Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim."
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
  "entrypoint": "solution.interpolate_motion",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract."
    },
    "axes": "Batch, transition, joint and quaternion axes specified in the contract",
    "timestamp_assumptions": "Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents.",
    "batching": "Batch, transition, joint and quaternion axes specified in the contract"
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
    "authoring_notes": "Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.",
    "primary_urls": [
      "https://arxiv.org/abs/1804.02717"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2018-deepmimic.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Interpolate a Reference Motion Pose

## Contract

`times` is real `(T,)`, `positions` is real `(T, 3)`, `rotations` is real `(T, J, 4)` and `query_times` is real `(Q,)`. Bounds are `2 <= T <= 1024`, `1 <= J <= 32` and `0 <= Q <= 256`. Timestamps must increase strictly and lie in `[0, 1_000_000]` seconds; queries have the same range. Positions are root translations in meters in a right-handed, y-up world. Each rotation is a scalar-first `(w, x, y, z)` quaternion for a joint relative to its parent. Require its norm within `1e-6` of one, then normalize it.

Clamp each query to the clip endpoints. Choose the lower segment with `searchsorted(times, clamped_query, side="right") - 1`, clipped to `[0, T-2]`; compute its fractional time alpha. Interpolate positions linearly. For each joint, negate the high-end quaternion if its dot product with the low-end quaternion is negative. Use shortest-arc SLERP, except that dot products greater than `0.9995` use normalized linear interpolation. Normalize every output quaternion.

Return a dictionary with `positions` (float64 `(Q, 3)`), `rotations` (float64 `(Q, J, 4)`), `interval` (int64 `(Q,)`) and `alpha` (float64 `(Q,)`). Quaternion endpoint signs follow the segment sign rule; they need not match raw source signs. Empty queries are valid. Do not wrap the clip, synthesize velocities or retarget motion.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
