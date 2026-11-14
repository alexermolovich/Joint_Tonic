---
{
  "schema_version": 1,
  "problem_id": "dreureka-reward-expression-program",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Validate a Generated Reward Program",
  "summary": "A small arithmetic reward language makes each generated term inspectable.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-dr-eureka",
    "policy-components"
  ],
  "paper_ids": [
    "2024-dr-eureka"
  ],
  "paper_sections": [
    "Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer."
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
  "entrypoint": "solution.evaluate_reward_expression",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Reward contributions and independent progress/success metrics are dimensionless and already normalized."
    },
    "axes": "Batch, rollout, time and component axes are defined in the contract",
    "timestamp_assumptions": "Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit.",
    "batching": "Batch, rollout, time and component axes are defined in the contract"
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
    "authoring_notes": "Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.",
    "primary_urls": [
      "https://arxiv.org/abs/2406.01967"
    ],
    "paper_card": "research/papers/robot-learning-rl/2024-dr-eureka.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Validate a Generated Reward Program

## Contract

expression is built-in str of length 1..512, parsed as a Python expression but never executed with eval/exec. features is dict with 1..16 keys matching ASCII [a-z][a-z0-9_]{0,31}, values real (B,) with shared 0<=B<=4096, finite abs<=100. Allowed AST: Expression, binary +,-,*, unary +,-, feature Name, numeric literal built-in int/float excluding bool with finite abs<=100; parentheses only group. Maximum 128 AST nodes (including operator/context nodes from ast.walk), maximum 16 expression-value levels excluding outer Expression: each leaf depth 1; operator depth 1+max child depth. Reject all other syntax and unknown names, including in empty batches. Validate every produced array element finite abs<=1e6; no clipping. With B=0 these elementwise bounds are vacuous, but syntax, literal bounds, feature names, node count and depth are always checked before evaluation. Return dict reward float64(B,), used_features list[str] sorted unique referenced feature names, node_count Python int len(list(ast.walk(tree))). Numeric constant expressions broadcast to B. This original restricted arithmetic language provides inspectable reward formulas; it is not a security sandbox for arbitrary Python, a complete generated reward function, or a claim about the paper's program grammar.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
