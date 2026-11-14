---
{
  "schema_version": 1,
  "problem_id": "paired-linear-image-attention",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Apply Paired-Image Self and Cross Attention",
  "summary": "Apply a bounded paired-image self-attention stage followed by simultaneous cross-attention.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "loftr"
  ],
  "paper_ids": [
    "2021-loftr"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2021-loftr"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.paired_attention",
  "physical_contract": {
    "frames": [
      "Image pixel coordinates x right, y down; feature channels dimensionless"
    ],
    "units": {
      "values": "Pixels for geometry, dimensionless confidence and descriptors"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "ec525c46af5a6245a9246807dc0b7b38192aa3f3778db7e314a6b1501862813e"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2104.00680"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Apply Paired-Image Self and Cross Attention

Implement `paired_attention(source, target, weights, source_valid, target_valid)`.

Apply a bounded paired-image self-attention stage followed by simultaneous cross-attention.

`source (N,D)` and `target (M,D)` are float64, `0<=N,M<=256`, `1<=D<=32`, absolute entries <=10. `weights` is float64 `(4,D,D)` ordered `[Wq,Wk,Wv,Wo]`, absolute entries <=2. `source_valid (N,)` and `target_valid (M,)` are bool masks. Feature channels are dimensionless; positions have already been encoded by the caller if desired.

Use positive feature map `phi(z)=z+1` for z>=0, else exp(z). For queries X and context Y, form Q=phi(X@Wq), K=phi(Y@Wk), V=Y@Wv. Exclude invalid context rows from K and V. Compute message `(Q@(K.T@V))/maximum(Q@sum(K,axis=0),1e-9)`, dividing each output row by its scalar denominator, then multiply by Wo. Zero messages for invalid queries; an empty or fully masked context gives zero messages. Compute phi without overflowing exponentials on unused positive branches.

First zero all invalid input rows to obtain A0,B0. Compute A1=A0+attention(A0,A0), B1=B0+attention(B0,B0). Then compute A2=A1+attention(A1,B1) and B2=B1+attention(B1,A1), using the same frozen A1,B1 for BOTH cross updates.

Return fresh float64 `self_source (N,D)`, `self_target (M,D)`, `source (N,D)=A2`, `target (M,D)=B2` in a dictionary. Invalid rows remain zero. This shared-weight, single-head residual block illustrates LoFTR's positive-feature linear attention mechanism. It deliberately omits learned positional encoding, layer normalization, feed-forward blocks and full multi-head architecture.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With all four weight matrices zero, outputs equal the supplied feature rows wherever valid and are zero elsewhere. The messages are zero.
2. D=1, all four weights 1, one valid source feature `[[1.]]`, one valid target feature `[[2.]]`: self_source is `[[2.]]`, self_target `[[4.]]`, and both final outputs are `[[6.]]`. Sequentially updating the target from an already updated source would be wrong.

## Source and scope

[Primary source](https://arxiv.org/abs/2104.00680). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute masked key/value summaries for each self and cross message. Save both self outputs before either cross update. Runtime O((N+M)D^2), avoiding materializing NM similarities; working storage O((N+M)D+D^2).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
