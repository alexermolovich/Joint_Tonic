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
