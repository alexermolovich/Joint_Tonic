---
{
  "schema_version": 1,
  "problem_id": "deepmimic-pose-velocity-rewards",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute Pose and Velocity Imitation Rewards",
  "summary": "Motion imitation should compare physical orientations, not quaternion storage signs.",
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
  "entrypoint": "solution.imitation_rewards",
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

# Compute Pose and Velocity Imitation Rewards

## Contract

`rotations` and `reference_rotations` are real `(B, J, 4)`; `velocities` and `reference_velocities` are real `(B, J, 3)`, with `1 <= B <= 128` and `1 <= J <= 32`. Rotations are scalar-first `(w, x, y, z)` parent-local joint quaternions. Require norms within `1e-6` of one and then normalize. Angular velocities are in radians/second in corresponding parent-local frames; no frame conversion is implicit.

For each joint, angle error is `2*arccos(clip(abs(dot(q, q_reference)), 0, 1))` radians. Return `angle_error` as float64 `(B, J)`, `pose` as float64 `(B,)` equal to `exp(-2*sum(angle_error**2, axis=1))`, and `velocity` as float64 `(B,)` equal to `exp(-0.1*sum((velocity-reference_velocity)**2, over joints and axes))`, in a dictionary.

The coefficients carry reciprocal squared units so rewards are dimensionless. This isolates DeepMimic's pose and velocity terms. Do not add end-effector or center-of-mass terms, or claim this is the complete imitation reward.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
