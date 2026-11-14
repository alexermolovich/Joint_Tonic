---
{
  "schema_version": 1,
  "problem_id": "dreamer-continuation-lambda-returns",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Build Lambda-Return Targets",
  "summary": "An imagined transition may continue only with some predicted probability.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-dreamerv3",
    "policy-components"
  ],
  "paper_ids": [
    "2023-dreamerv3"
  ],
  "paper_sections": [
    "A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark."
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
  "entrypoint": "solution.imagined_lambda_returns",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats."
    },
    "axes": "Batch, categorical-group, category, rollout-time and latent axes are defined in the contract",
    "timestamp_assumptions": "Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion.",
    "batching": "Batch, categorical-group, category, rollout-time and latent axes are defined in the contract"
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
    "authoring_notes": "A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.",
    "primary_urls": [
      "https://arxiv.org/html/2301.04104v2"
    ],
    "paper_card": "research/papers/robot-learning-rl/2023-dreamerv3.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Build Lambda-Return Targets

## Contract

rewards, next_values, continuation real(B,T), valid Boolean same shape;1<=B<=64,1<=T<=1024; rewards/values abs<=1e6,continuation[0,1], gamma/lam scalar[0,1]. Validity forms prefix per row (possibly empty). next_values[t] is value at transition t's successor latent state; continuation[t] is predicted probability of continuing through that transition. In reverse, recursive_next is G[t+1] when next slot valid, otherwise next_values[t]; G[t]=r[t]+gamma*c[t]*((1-lam)*next_values[t]+lam*recursive_next). Return float64(B,T), zero invalid. Every invalid-mask numeric input still validated. Last valid step bootstraps its successor value. This explicit next-state indexing distinguishes the task from some paper notation. Fractional predicted continuation is essential; existing PPO Boolean terminal/truncation task is only a prerequisite.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
