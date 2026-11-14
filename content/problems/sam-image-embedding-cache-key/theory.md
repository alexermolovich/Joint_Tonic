# Reuse Image Embeddings Without Stale-Cache Errors

## Intuition

An image embedding can be reused only when the image, encoder and preprocessing recipe agree. A content-addressed key makes these dependencies explicit. The key decides identity; it does not prove that bytes loaded from storage are a valid embedding.

## Mathematics and physical meaning

Let $h_I,h_E,h_P$ be 64-character lowercase SHA-256 identifiers for image bytes, encoder artifact and preprocessing recipe. Let $(H',W')$ be the resized image dimensions. Define a record $R$ with exactly the documented five fields: schema, three hashes and resized shape. The key is
$$k=\operatorname{SHA256}(\operatorname{ASCII}(\operatorname{canonicalJSON}(R))).$$
Canonical JSON sorts keys, uses comma/colon separators without spaces, writes schema as integer 1 and shape as a two-element list. This fixes the exact byte representation; semantically equivalent but differently formatted JSON has a different digest.

For optional stored key $k_c$, the output is $\mathrm{hit}=(k_c=k)$. A missing key always misses. Neither wall-clock time nor a file path participates; immutable artifact digests represent changes. Shape is in pixel counts and no spatial transform or model inference occurs.

## Visual trace

| Dependency | Same artifact | Changed artifact |
|---|---|---|
| Image bytes | same hash | different key |
| Encoder weights | same hash | different key |
| Resize/normalization recipe | same hash | different key |
| Resized shape | same tuple | different key |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** Use image hash `"0"*64`, encoder hash `"1"*64`, preprocessing hash `"2"*64` and shape `(4, 8)`. With cached key `None`, return the SHA-256 of the documented canonical record and `hit=False`. Reusing that returned digest as the cached key gives the same digest and `hit=True`.

**Example 2.** Change only preprocessing hash to `"3"*64` while keeping the original cached key. The new digest differs and `hit=False`; unchanged image bytes alone are insufficient.

## Why this matters on a robot

Reusing a SAM embedding after changing normalization can silently misalign prompt results. Image-only cache keys miss this dependency. A storage layer must separately verify the embedding's own checksum and access policy.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2304.02643). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
