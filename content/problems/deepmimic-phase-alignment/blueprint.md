---
{
  "schema_version": 1,
  "problem_id": "deepmimic-phase-alignment",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Detect Phase Misalignment in a Motion Clip",
  "summary": "Two phases close to opposite ends of a cyclic clip can still describe nearly the same point in the motion.",
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
  "entrypoint": "solution.phase_alignment",
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

# Detect Phase Misalignment in a Motion Clip

## Contract

`observed_phase` and `reference_phase` are real `(B, T)`, with `1 <= B <= 128`, `1 <= T <= 256` and phase values in `[0, 1)`. `valid` is a Boolean array of the same shape; `threshold` is a scalar in `[0, 0.5]` clip fractions.

Compute signed circular error as `((observed - reference + 0.5) % 1) - 0.5`, in `[-0.5, 0.5)`. The half-cycle tie is represented as -0.5. Return a dictionary with `error` (float64 `(B, T)`, NaN at invalid samples), `misaligned` (Boolean `(B, T)`, true only for valid samples whose absolute error strictly exceeds the threshold), `mean_absolute` (float64 `(B,)`, mean over each row's valid samples, or NaN when absent) and `counts` (int64 `(B,)`).

Samples refer to aligned moments in the same cyclic clip. This original diagnostic does not align clips, solve time warping or establish successful pose tracking.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
