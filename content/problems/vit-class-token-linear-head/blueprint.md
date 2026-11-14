---
{
  "schema_version": 1,
  "problem_id": "vit-class-token-linear-head",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Read a Normalized Class Token with a Linear Head",
  "type": "function",
  "difficulty": "medium",
  "paper_ids": [
    "2021-vision-transformer"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2021-vision-transformer"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.class_token_logits",
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
      "Model feature coordinates; no physical frame transform"
    ],
    "units": {
      "features_logits": "dimensionless"
    },
    "axes": "B batch, L tokens, D channels, C output classes; token zero only",
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
    "evaluator_sha256": "83c97db88c1fa6775caa31e4675b532990d15de1d164e939793bc1dda7e5f470"
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
  }
}
---

# Read a Normalized Class Token with a Linear Head

The class token summarizes a transformer sequence. This readout normalizes only that token across its channels and applies a linear classifier. Patch tokens remain in the input because they helped create the class token upstream, but this function must not average them again.

```python
def class_token_logits(tokens, gamma, beta, weight, bias, epsilon):
    ...
```

## Function contract

Inputs: `tokens: float64(B, L, D)`, `gamma: float64(D,)`, `beta: float64(D,)`, `weight: float64(D, C)`, `bias: float64(C,)` and a Python real `epsilon` in `[1e-8, 1]`. Bounds: `1<=B<=32`, `1<=L<=257`, `1<=D, C<=64`.

Take `tokens[:, 0]` as the class token. Apply population layer normalization across its D channels, with denominator `sqrt(variance + epsilon)`, then the supplied channel scale/offset and linear head. Return fresh `float64(B, C)` logits. Do not apply softmax, average other tokens, or use sample variance. Validate all input tokens even though only index zero contributes. All features and parameters are dimensionless model coordinates.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Class token `[1, 3]`, gamma `[1, 1]`, beta `[0, 0]`, identity head, zero bias and epsilon `1` produce logits `[[-1/sqrt(2), 1/sqrt(2)]]`.

**Example 2.** Any one-channel token, gamma `[2]`, beta `[3]`, weight `[[4]]`, bias `[5]` and epsilon `1e-8` produce `[[17]]`: the normalized one-channel value is zero.

## Source and scope

Original bounded component based on [2021-vision-transformer](https://arxiv.org/abs/2010.11929). A frozen visual encoder can feed a small robot scene classifier. Averaging all tokens here changes the learned readout contract; normalizing across batches also makes one robot's prediction depend on another sample.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
