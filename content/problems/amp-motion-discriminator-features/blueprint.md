---
{
  "schema_version": 1,
  "problem_id": "amp-motion-discriminator-features",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Construct Motion Discriminator Features",
  "summary": "A motion discriminator should recognize coordinated movement regardless of where the character stands or which way it faces.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2021-adversarial-motion-priors",
    "policy-components"
  ],
  "paper_ids": [
    "2021-adversarial-motion-priors"
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
  "entrypoint": "solution.motion_features",
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
      "https://arxiv.org/abs/2104.02180"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2021-adversarial-motion-priors.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Construct Motion Discriminator Features

## Contract

Root positions, root linear velocities and root angular velocities are real `(B, 2, 3)` arrays. `root_yaw` is real `(B, 2)`. `joint_rotations` is real `(B, 2, J, 3, 3)`, `joint_velocities` is real `(B, 2, J, 3)`, and `endpoints` is real `(B, 2, E, 3)`. Bounds are `1 <= B <= 64`, `1 <= J <= 32`, `1 <= E <= 8`. Transition index 0 is current; 1 is successor.

The world is right-handed with +y up. Local +x is the heading direction. Yaw is in `[-pi, pi]` radians and defines the local-to-world matrix `Ry = [[cos(yaw), 0, sin(yaw)], [0, 1, 0], [-sin(yaw), 0, cos(yaw)]]`. Positions are meters, root linear velocities meters/second, and angular velocities radians/second. Joint rotations are parent-local proper rotation matrices: validate orthogonality and determinant one with absolute tolerance `1e-6`, zero relative tolerance. Joint velocities are already parent-local.

For each state, concatenate these feature blocks in order:

1. `Ry.T @ root_velocity` (3 entries).
2. `Ry.T @ root_angular_velocity` (3 entries).
3. For each joint in order, its rotation's first column followed by its second column (6J entries).
4. Joint velocities flattened in joint/axis order (3J entries).
5. `Ry.T @ (endpoint - root_position)` for each endpoint in order (3E entries).

Return a fresh float64 `(B, 2F)` array, where `F = 6 + 9J + 3E`, containing current features followed by successor features. Each state uses its own root origin and heading. Do not include root height or clip phase, normalize features, or train a discriminator. The six-dimensional rotation ordering is an explicit teaching convention consistent with a normal/tangent representation; released checkpoint compatibility is not claimed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
