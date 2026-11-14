---
{
  "schema_version": 1,
  "problem_id": "rt2-constrained-action-decoding",
  "content_version": "0.1.0",
  "status": "drafted",
  "title": "Constrain Autoregressive Decoding to Valid Actions",
  "summary": "Constrain Autoregressive Decoding to Valid Actions",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2023-rt-2",
    "policy-interface"
  ],
  "paper_ids": [
    "2023-rt-2"
  ],
  "paper_sections": [
    "Section 3.2: Output Constraint"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "rt2-parse-action-grammar"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build",
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
  "entrypoint": "solution.constrained_action_step",
  "physical_contract": {
    "frames": [
      "Caller-declared aligned visual/action interface; no physical frame transformation"
    ],
    "units": {
      "features": "dimensionless learned coordinates",
      "tokens": "dimensionless IDs where applicable"
    },
    "axes": "Explicit shapes and token/feature ordering in statement.md",
    "timestamp_assumptions": "One aligned observation context; no internal clock or controller execution",
    "batching": "Batch-first; empty batch only in the constrained decoding task"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-06,
    "atol": 1e-07,
    "exact_fields": [
      "selected token IDs and Boolean masks"
    ],
    "public_case_families": [
      "two-worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "typed-boundary-validation",
      "noncontiguous-inputs",
      "independent-oracle",
      "storage-and-nonmutation",
      "gradients-where-required",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded contract; source mechanisms and teaching deviations are explicit. No full trained policy or paper benchmark is reproduced.",
    "primary_urls": [
      "https://arxiv.org/html/2307.15818v1"
    ],
    "paper_card": "research/papers/vla-embodied/2023-rt-2.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": []
}
---

# Constrain Autoregressive Decoding to Valid Actions

Implement constrained_action_step(logits, vocabulary, positions, channels), returning (tokens, probabilities).

logits is a finite NumPy float64 array (B,V), with 0 <= B <= 256, 4 <= V <= 65536, at most 1,000,000 entries, and absolute values <= 100. vocabulary is a NumPy int64 array (K,), with 2 <= K <= min(4096,V-2), containing unique token IDs in [2,V). Its order may be arbitrary. positions is int64 (B,). channels is a built-in int excluding bool, in [1,64], and each position is in [0,channels]. Noncontiguous arrays are valid.

This follows the existing original fixed-width action grammar: position 0 is a termination flag with allowed IDs {0,1}; positions 1 through channels are action fields with allowed IDs from vocabulary. A termination flag of 1 does not remove the remaining fields. The current position is supplied, not inferred from an input sequence. No other token is allowed at that position.

For each row, softmax only its allowed logits, with all forbidden probabilities exactly zero. Return probabilities as a new float64 array (B,V), and tokens as a new int64 array (B,) selecting the allowed maximum logit. If allowed logits tie, choose the smallest numeric token ID, independently of vocabulary ordering. No sampling, temperature parameter, beam search, language-model call or full-sequence generation is included. Empty B returns the corresponding empty arrays.

Preserve inputs, use independent storage for both outputs, and validate the entire batch before returning. Non-array logits/vocabulary/positions raises TypeError; all other violations, including invalid channels, raise ValueError. Scores, probabilities, IDs and field positions are dimensionless. Physical action bounds, channel order, frame and control period belong to the upstream codec. This teaching grammar is not an exact RT-2 tokenizer, and grammar-valid output does not establish robot safety.

## Implementation and evaluator plan

Review the complete mathematical and physical contract before implementation. Use independent scalar/tensor oracles, both worked examples, stated invalid-input behavior, aliasing checks and analytical gradients where applicable. Verify the reference through actual isolated Run and Submit and reject the starter before publication. No new runtime dependency or model checkpoint is needed.
