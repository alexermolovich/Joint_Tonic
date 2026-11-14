# Reproduce a Model from an Immutable Run Manifest

## Intuition

A run name such as latest is convenient for browsing but cannot identify a reproducible experiment. A replay needs fixed content, versions and randomness. This exercise implements the preflight boundary: compare what was declared with what is actually supplied before executing any training.

## Identity checks, not filenames

For expected artifact names K, let $h_k$ be the declared digest and $b_k$ the supplied byte string. Byte identity is checked through

$$
H(b_k)=h_k,\qquad H=\operatorname{SHA256}.
$$

Assuming the digest is trustworthy, a mismatch reveals changed bytes even when the name is unchanged. Hashing bytes avoids ambiguities from newline normalization, decoding or JSON formatting. A hash is an integrity identifier, not a signature proving who authored the file.

Let E be the expected environment-name set and $v_j$ its declared version strings. A matching preflight requires

$$
K_{\mathrm{actual}}=K,\quad E_{\mathrm{actual}}=E,\quad
\bigwedge_{k\in K} H(b_k)=h_k,\quad
\bigwedge_{j\in E} v_j^{\mathrm{actual}}=v_j,\quad
s_{\mathrm{actual}}=s_{\mathrm{manifest}}.
$$

The seed s is an unsigned32 integer. This function compares it; it does not seed an RNG. Exact string comparison prevents silently substituting an allegedly compatible runtime.

## Visual: the replay boundary

| Declared input | Observed value | Evidence |
|---|---|---|
| weights digest for empty bytes | b"x" | digest_mismatch |
| Python3.12.3 | Python3.11.0 | version_mismatch |
| seed7 | seed8 | mismatch |

Read across each row to locate a distinct repair. An unexpected artifact contributes an additional row in example2. This table is the static pipeline view and text alternative: manifest plus observations produce discrepancy rows, then a caller decides whether to launch.

## Why this matters on a robot

Replaying an evaluation with different calibration bytes or a different simulator version can alter the apparent safety margin. Pinning only model weights is insufficient. Even matching this manifest cannot guarantee identical results: omitted compiler flags, hardware kernels, nondeterministic operations or external services can still change behavior. The manifest author must include all relevant artifacts and environment identities, and numerical reproducibility remains a separate evaluation.

## Check your understanding

1. Does matching a digest authenticate the artifact's author?
2. Does an empty discrepancy list prove bitwise-identical training weights?

## Sources and prerequisites

This is a bounded preflight component of model reproduction, motivated by TFX pipeline integration. It validates supplied bytes/versions/seed and deliberately does not run training or promise bitwise-identical weights. The manifest schema and rejection vocabulary are original. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/), Section2.2 pipeline integration; Section3 data/transform/model stages. Prerequisites: [record-artifact-lineage](/problems/record-artifact-lineage); no Python or mathematics tutorial is assumed.
