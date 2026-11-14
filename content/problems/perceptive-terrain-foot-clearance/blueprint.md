---
{
  "schema_version": 1,
  "problem_id": "perceptive-terrain-foot-clearance",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Foot Clearance Across Terrain Slices",
  "summary": "Foot height becomes useful only relative to the nearby support surface.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2022-perceptive-locomotion",
    "policy-components"
  ],
  "paper_ids": [
    "2022-perceptive-locomotion"
  ],
  "paper_sections": [
    "Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic."
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
  "entrypoint": "solution.terrain_clearance_report",
  "physical_contract": {
    "frames": [
      "Action vectors use identical robot joint order; foot and support heights share a right-handed world frame with z up"
    ],
    "units": {
      "values": "Action targets and action scales use radians. Environmental features and their scales share declared normalized coordinates. Foot positions, terrain heights and clearance thresholds use meters; resulting normalized losses and violation rates are dimensionless."
    },
    "axes": "Batch B, synchronized time T, and declared action, environmental-feature or foot axes",
    "timestamp_assumptions": "Times are already aligned within each environment. A terrain label is constant across one supplied window. No resampling, recurrent state estimation or simulator stepping occurs.",
    "batching": "Batch B, synchronized time T, and declared action, environmental-feature or foot axes"
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
    "authoring_notes": "Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic.",
    "primary_urls": [
      "https://arxiv.org/abs/2201.08117"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2022-perceptive-locomotion.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Evaluate Foot Clearance Across Terrain Slices

## Contract

Implement `terrain_clearance_report(foot_positions, terrain_height, swing, observed, terrain_ids, minimum_clearance, num_terrains)`.

Foot positions real(B,T,F,3),0<=B<=128,1<=T<=256,1<=F<=4; terrain_height real(B,T,F), all meters abs<=1e4 in one right-handed world frame with z up and matched timestamps. Height is a supplied support-surface estimate directly under each foot; no map interpolation. Swing/observed bool(B,T,F),eligible=swing AND observed. Terrain IDs integer(B,)0..K-1; num_terrains builtinintK1..64; minimum_clearance real(K,) meters[0,1]. Clearance=foot_z-height. Return dict clearance float64(B,T,F) NaN outside eligible, counts int64(K,),mean_clearance/min_clearance/violation_rate float64(K,),NaN for absent terrain; violation when clearance<minimum_clearance[terrain] (equality passes). Aggregate each eligible FOOT/TIME sample equally, not episode means or dwell-time weights. Every environment retains one terrain ID throughout this supplied window. Negative clearance remains negative and counts as a violation; contact/stance samples are excluded. This is an original terrain-slice diagnostic, not a collision detector or proof that a gait is safe. Terrain height error can directly bias the metric.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
