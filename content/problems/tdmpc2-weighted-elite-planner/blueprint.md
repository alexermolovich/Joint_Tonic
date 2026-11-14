---
{
  "schema_version": 1,
  "problem_id": "tdmpc2-weighted-elite-planner",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Update a Sampling-Based Planner",
  "summary": "A sampling planner concentrates its next proposal around high-scoring candidate sequences.",
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
  "entrypoint": "solution.update_elite_distribution",
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

# Update a Sampling-Based Planner

## Contract

actions real(K,H,A) normalized[-1,1],scores real(K,)abs<=1e6,valid bool(K,);1<=K<=1024,1<=H<=64,1<=A<=32,total action entries<=1e6; num_elites built-in int1..K,require validcount>=num_elites; inverse_temperature scalar[0,100],min_std/max_std scalar0<=min<=max<=2. Select num_elites valid candidate indices by descending score then ascending original index. Compute normalized weights exp(inverse_temperature*(score-max_elite_score)). Return dict elite_indices int64(E,),weights float64(E,),mean float64(H,A)=weighted mean of eliteactions,std float64(H,A)=sqrt(weighted population variance around NEW mean),clamped[min_std,max_std]. Exact normalization (no extra denominator epsilon since at least one exponential=1). No oldmean momentum, randomsampling, actionselection or control execution. Supplied scores use a fixed dimensionless reward scale so inverse_temperature has reciprocal score units. Current official MPPI-style update motivates the component; deterministic ties and omitted tiny denominator epsilon are declared original conventions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
