---
{
  "schema_version": 1,
  "problem_id": "grounding-bidirectional-cross-attention",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention",
  "type": "function",
  "difficulty": "hard",
  "paper_ids": [
    "2023-grounding-dino"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2023-grounding-dino"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.bidirectional_context",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator"
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
  "physical_contract": {
    "frames": [
      "Aligned projected image/text features for the same observation"
    ],
    "units": {
      "features_weights": "dimensionless"
    },
    "axes": "B batches,P image tokens,T text tokens,D shared channels",
    "timestamp_assumptions": "Fixed supplied batch; cameras/observations are aligned by caller. No clock inference, state history or real-time guarantee.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-mechanism-oracle",
      "boundary-and-invalid-input",
      "maximum-advertised-dimensions",
      "input-preservation-and-output-aliasing"
    ],
    "performance_class": "none",
    "evaluator_sha256": "f62e73301532ea89cc047232214c40dd94e7b26983f443784d772bb5fbb2fafb"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.05499"
    ],
    "implementation_urls": []
  }
}
---

# Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention

Image-to-text and text-to-image attention answer different questions. Each image token asks which words describe it; each word asks which image locations support it. The two directions share raw compatibility scores but normalize across different keys.

```python
def bidirectional_context(image_tokens, text_tokens, image_valid, text_valid):
    ...
```

## Function contract

Inputs: `image_tokens: float64(B, P, D)`, `text_tokens: float64(B, T, D)`, `image_valid: bool(B, P)` and `text_valid: bool(B, T)`. Bounds: `1<=B<=8`, `1<=P<=128`, `1<=T<=64`, `1<=D<=64`. Tokens are supplied projected dimensionless features with aligned batches/observations.

Compute compatibility scores `image_tokens @ text_tokens.transpose(0, 2, 1) / sqrt(D)`. Each valid image query applies stable softmax over valid text keys. Independently, each valid text query applies softmax to the transposed scores over valid image keys. Invalid queries and rows with no valid keys have exact zero weights and context.

Return four float64 arrays: `image_context(B, P, D)`, `text_context(B, T, D)`, `image_weights(B, P, T)` and `text_weights(B, T, P)`. Context is each weight matrix multiplied by the opposite modality's tokens. Do not add learned projections, multiple heads, residual gates or feed-forward layers.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One image token `[1]` and two text tokens `[0]`, `[0]`, all valid: image weights `[.5,.5]`, image context `[0]`; each text query has weight `[1]` and context `[1]`.

**Example 2.** Make both text tokens invalid. Image queries have no valid keys and text queries are invalid; every returned context and weight is zero, without NaNs.

## Source and scope

Original bounded component based on [2023-grounding-dino](https://arxiv.org/abs/2303.05499). Language grounding connects a phrase such as 'red handle' to visible regions. Simply transposing image-to-text probabilities does not yield text-to-image probabilities. Including padded tokens can shift grounding even when the real words are unchanged.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
