---
{
  "schema_version": 1,
  "problem_id": "rt2-serialize-action-tokens",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Serialize Robot Actions as Discrete Tokens",
  "summary": "Serialize Robot Actions as Discrete Tokens",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 35,
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
    "Section3.2: Robot-Action Fine-tuning"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "rt1-action-codec"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
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
  "entrypoint": "solution.serialize_action_tokens",
  "physical_contract": {
    "frames": [
      "Caller-declared normalized action interface; no frame conversion"
    ],
    "units": {
      "tokens": "dimensionless integer IDs",
      "actions": "normalized Euclidean channels",
      "flow_time": "dimensionless, separate from controller timestamps"
    },
    "axes": "Shapes and ordering defined explicitly in statement.md",
    "timestamp_assumptions": "One aligned control observation per batch item; fixed horizon interval provided upstream",
    "batching": "Batch-first; empty batch supported only for token grammar tasks"
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "dtype-shape-range-validation",
      "ordering",
      "noncontiguous-and-storage",
      "empty-where-supported",
      "independent-oracle",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded component contract inspired by the cited mechanism; no full trained policy or physical evaluation is reproduced.",
    "primary_urls": [
      "https://arxiv.org/abs/2307.15818"
    ],
    "implementation_urls": []
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": [
    "code_issue_scout"
  ]
}
---

# Serialize Robot Actions as Discrete Tokens

## Contract

Implement serialize_action_tokens(bins, vocabulary, termination). bins has shape(B,D) and every entry lies in[0,K). termination has shape(B,) and contains only0 or1. Return tokens(B,D+1): first copy termination, then map each bin q to vocabulary[q]. Do not sort the vocabulary or add an assumed fixed vocabulary offset.

Array inputs must be NumPy int64, not lists, bool arrays, floating arrays or int32. All output arrays use int64 and fresh independent storage; preserve inputs and support noncontiguous arrays. B may be zero and is at most1024; D is in[1,64]. The supplied vocabulary has shape(K,),2<=K<=4096, contains unique integer token IDs in[2,1_000_000], and explicitly excludes the reserved termination IDs0 and1.

The format is an original teaching grammar inspired by RT-2's action-token interface, not the exact pretrained tokenizer of either RT-2 model. Each row is [termination,channel0,...,channelD-1]. Termination0 means continue and1 means terminate; D action fields are required in either case. Values are already quantized bins: no physical quantization, detokenization to actuator units, text parsing, special BOS/EOS tokens or actual execution occurs. Channel order, frame, control period and normalization are fixed by the upstream action codec.

Raise TypeError for a non-array argument. Raise ValueError for every dtype/shape/value/vocabulary/grammar violation. Reject the whole batch if any row is invalid; do not return partial successes.

## Reference and evaluator plan

Implement the declared deterministic interface, with independent fixture/oracle checks of ordering, boundaries, ownership and all documented errors. Public examples establish visible behavior; hidden cases test the same contract at additional shapes. Use the actual local bubblewrap runtime for Run and Submit. No new dependencies or external assets. Static tables and original display math provide the theory visual; synthetic fixtures are CC0-1.0.
