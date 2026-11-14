---
{
  "schema_version": 1,
  "problem_id": "tdmpc2-candidate-trajectory-scores",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Score Candidate Action Trajectories",
  "summary": "A candidate plan earns predicted rewards until its first terminal transition.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-td-mpc2",
    "policy-components"
  ],
  "paper_ids": [
    "2023-td-mpc2"
  ],
  "paper_sections": [
    "Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller."
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
  "entrypoint": "solution.score_latent_trajectories",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units."
    },
    "axes": "Batch, horizon, action, latent-group, critic and bin dimensions are defined in the contract",
    "timestamp_assumptions": "Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution.",
    "batching": "Batch, horizon, action, latent-group, critic and bin dimensions are defined in the contract"
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
    "authoring_notes": "Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.16828"
    ],
    "paper_card": "research/papers/robot-learning-rl/2023-td-mpc2.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Score Candidate Action Trajectories

## Contract

rewards real(K,H),terminated bool(K,H),terminal_values real(K,),gamma scalar[0,1];1<=K<=1024,0<=H<=128;absvalues<=1e6. Reward at step t occurs before terminated[t] ends that transition. Define alive initiallyTrue, weight[t]=gamma**t if all previous terminatedflagsFalse else0. Return dict contributions float64(K,H)=weight*reward; tail float64(K)=gamma**H*terminal_value if no termination in horizon else0; scores float64(K)=sum contributions+tail; best Pythonint argmax(scores),tie lowestindex. Any later rewards after first termination ignored but still numerically validated. With H0 score=terminal_value. Values already decoded from model predictions; no neural inference occurs here. This explicit Boolean termination extension matches current official episodic planner convention, not a claim about every2023 configuration.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
