---
{
  "schema_version": 1,
  "problem_id": "perceptive-teacher-belief-loss",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute Belief Reconstruction and Teacher-Action Losses",
  "summary": "A student can imitate a teacher action even when some environmental labels are unavailable.",
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
  "entrypoint": "solution.teacher_belief_loss",
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

# Compute Belief Reconstruction and Teacher-Action Losses

## Contract

Implement `teacher_belief_loss(student_actions, teacher_actions, reconstruction, privileged_target, action_valid, reconstruction_valid, action_scale, feature_scale, weights)`.

Student/teacher action arrays real(B,T,A),0<=B<=64,1<=T<=128,1<=A<=32, joint-position targets radians abs<=10 in identical robot joint order. Reconstruction/privileged_target real(B,T,D),1<=D<=64, normalized environmental coordinates abs<=100. Action_valid bool(B,T) selects complete action vectors; reconstruction_valid bool(B,T,D) selects individual environment labels. Action_scale real(A,) radians in[1e-3,10], feature_scale real(D,) in[1e-3,100] in the same normalized coordinate unit as feature; weights real(2,) in[0,100]. For action count na=A*sum(action_valid), action loss is sum(valid*((student-teacher)/action_scale)^2)/na; for feature count nf=sum(reconstruction_valid), feature loss is sum(valid*((reconstruction-target)/feature_scale)^2)/nf. Each absent component has loss0, no fabricated labels. Total L=weights[0]*La+weights[1]*Lf. Return dict components float64(2,),counts int64(2,),loss Pythonfloat, action_gradient float64(B,T,A),reconstruction_gradient float64(B,T,D) analytical total-L derivatives wrt STUDENT predictions only, zero outside masks and zero when component absent. Teacher targets and scales are fixed. Gradient action=2*w0*(student-teacher)/(na*action_scale^2), analogous feature. Original scale-normalized masked teaching objective, not the exact paper hyperparameters/architecture or a hardware controller.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
