---
{
  "schema_version": 1,
  "problem_id": "vit-pre-norm-block",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Assemble a Pre-Norm Vision Transformer Block",
  "summary": "Implement a single-head, dropout-free pre-norm transformer encoder block with supplied parameters.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "vision-transformer",
    "vit-pre-norm-block"
  ],
  "paper_ids": [
    "2021-vision-transformer"
  ],
  "paper_sections": [
    "Vision Transformer encoder architecture and image-resolution scaling"
  ],
  "track_ids": [
    "paper-2021-vision-transformer"
  ],
  "prerequisite_problem_ids": [
    "vit-patch-class-tokens"
  ],
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
  "entrypoint": "solution.vit_block",
  "physical_contract": {
    "frames": [
      "Ordered patch/class token features"
    ],
    "units": {
      "values": "dimensionless embeddings"
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
    "evaluator_sha256": "005579c9ebb80b62d72427cbbbe085446db56689dbf13f2c4e437e2d7066619f"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2010.11929"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Assemble a Pre-Norm Vision Transformer Block

Implement `vit_block(tokens: np.ndarray, parameters: dict) -> np.ndarray`.

Implement a single-head, dropout-free pre-norm transformer encoder block with supplied parameters.
tokens float64 (N,D),1<=N<=128,1<=D<=64, are dimensionless patch/class embeddings in fixed order. parameters is exactly a dict with float64 arrays: q,k,v,o (D,D), w1 (D,F),b1(F,),w2(F,D),b2(D,),gamma(2,D),beta(2,D),1<=F<=128. For each token, layer norm uses population variance and epsilon1e-5, then row-specific gamma/beta (row0 first norm,row1 second). Set z=LN0(tokens), attention=softmax((z@q)@(z@k).T/sqrt(D)) over keys, u=tokens+(attention@(z@v))@o. Return u+GELU(LN1(u)@w1+b1)@w2+b2, exact GELU(x)=0.5*x*(1+erf(x/sqrt2)). No qkv bias, attention mask, positional addition, final norm, dropout or multi-head split. All supplied values have absolute value<=100 (tighter than general rule). Return fresh float64(N,D).

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With q,k,v,o,w1,w2 and both biases all zero, gamma all ones and beta zeros, output equals tokens exactly: both residual branches contribute zero.
2. For one token `[2,4]`, zero attention branch and zero w1,w2, b2=`[1,-1]`, output is `[3,3]`. No final layer normalization is applied.

## Source and scope

[Primary source](https://arxiv.org/abs/2010.11929). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Use two pre-normalized residual branches with one-head attention and exact GELU. Time O(N²D+NDF), score storage O(N²).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
