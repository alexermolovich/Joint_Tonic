---
{
  "schema_version": 1,
  "problem_id": "sam-image-embedding-cache-key",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Reuse Image Embeddings Without Stale-Cache Errors",
  "type": "function",
  "difficulty": "easy",
  "paper_ids": [
    "2023-segment-anything"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2023-segment-anything"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.embedding_cache_key",
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
      "Artifact identity; no spatial transform"
    ],
    "units": {
      "resized_shape": "pixel counts",
      "hashes": "lowercase hexadecimal SHA-256"
    },
    "axes": "Exactly two shape entries height,width; no batch",
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
    "evaluator_sha256": "12772eec9a0a5e9b06b93d6ebf34884a7e5c61100c9113bf4639bd5f146ea6bc"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.02643"
    ],
    "implementation_urls": []
  }
}
---

# Reuse Image Embeddings Without Stale-Cache Errors

An image embedding can be reused only when the image, encoder and preprocessing recipe agree. A content-addressed key makes these dependencies explicit. The key decides identity; it does not prove that bytes loaded from storage are a valid embedding.

```python
def embedding_cache_key(image_sha256, encoder_sha256, preprocessing_sha256, resized_shape, cached_key):
    ...
```

## Function contract

The three artifact identifiers must be strings of exactly 64 lowercase hexadecimal characters. They identify image bytes, encoder artifact and preprocessing recipe. `resized_shape` must be exactly a tuple of two built-in integers in `[1, 8192]`, ordered `(height, width)`. `cached_key` is either `None` or another lowercase 64-character hexadecimal string.

Build exactly this record: `{"schema": 1, "image_sha256": image_sha256, "encoder_sha256": encoder_sha256, "preprocessing_sha256": preprocessing_sha256, "resized_shape": [height, width]}`. Serialize with sorted keys, separators `(',', ':')` and ASCII encoding. Compute its SHA-256 hexadecimal digest.

Return `{"key": digest, "hit": cached_key == digest}`, with Python `str` and `bool` values. This validates identity only: embedding integrity, storage lookup, model inference and freshness policy are outside scope. Hashes identify immutable artifacts, not filenames.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Use image hash `"0"*64`, encoder hash `"1"*64`, preprocessing hash `"2"*64` and shape `(4, 8)`. With cached key `None`, return the SHA-256 of the documented canonical record and `hit=False`. Reusing that returned digest as the cached key gives the same digest and `hit=True`.

**Example 2.** Change only preprocessing hash to `"3"*64` while keeping the original cached key. The new digest differs and `hit=False`; unchanged image bytes alone are insufficient.

## Source and scope

Original bounded component based on [2023-segment-anything](https://arxiv.org/abs/2304.02643). Reusing a SAM embedding after changing normalization can silently misalign prompt results. Image-only cache keys miss this dependency. A storage layer must separately verify the embedding's own checksum and access policy.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
