# Package and Verify an Edge Model Artifact

## Intuition

An edge deployment needs the exact model bytes and the preprocessing interface that produced its measurements. A manifest binds both in a deterministic representation so accidental changes are detectable.

## Two different hashes

Let M be model bytes, H SHA-256, and C deterministic canonical JSON encoding under the stated settings. First verify $h_m=H(M)$ against the expected digest. Then

$$h_{manifest}=H(C(\{model\_sha256:h_m,size\_bytes:|M|,metadata:Q\})).$$

Q contains format/runtime/input shape/dtype/calibration identity. Hash strings are lowercase hexadecimal, byte lengths count bytes, and input dimensions count elements. Never hash a manifest including its own digest; that would define a different circular problem.

## Visual: what each digest covers

| Evidence | Covered bytes/fields |
|---|---|
| Model SHA-256 | supplied model bytes only |
| Manifest SHA-256 | model digest, byte count, metadata |
| Calibration digest | recorded identifier; calibration bytes unavailable |

The table is the provenance diagram and text alternative. Changing runtime metadata changes the manifest hash even if model bytes stay identical.

## Why this matters on a robot

Deploying the right weights with the wrong input calibration can silently alter actions. Hashes detect mismatch relative to an expected identity; they do not authenticate a publisher. A signature and trust policy are separate mechanisms, deliberately absent here.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
