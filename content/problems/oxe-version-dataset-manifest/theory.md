# Version a Cross-Robot Dataset Manifest

## Intuition

A mixed dataset needs an identity that includes its versions, embodiments and calibration. Canonical serialization avoids treating harmless dictionary ordering as a new experiment while detecting changes that affect interpretation.

## Mathematical mechanism

Let P be the sorted validated manifest payload and C its canonical JSON byte string. Define $$h=\operatorname{SHA256}(\operatorname{UTF8}(C)).$$ Sorting record IDs and JSON keys removes insertion-order variation. The schema version belongs inside P, so changing interpretation rules changes h even if dataset records are unchanged.

## Visual computation trace

| Stage | Operation | Evidence |
|---|---|---|
| Records | validate unique IDs/versions/hashes | reject ambiguous source identity |
| Order | sort dataset IDs and JSON keys | order-independent bytes |
| Digest | SHA256 UTF-8 canonical JSON | reproducible snapshot ID |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

datasets=[], schema_version=1 returns canonical_json exactly `{"datasets":[],"schema_version":1}` and sha256 equal to SHA256 of those UTF-8 bytes. Empty manifests are allowed but contain no training data.

## Why this matters on a robot

A dataset name alone does not capture altered camera calibration or controller units. This function verifies syntax and content-addresses the manifest, not the existence or truth of referenced artifacts. Verify actual bytes at ingestion and record licenses separately.

## Physical contract and limits

Registry IDs, semantic versions and byte-content hashes have no physical units; calibration hashes identify externally pinned physical conventions. An immutable snapshot, not a mutable latest-version pointer; no wall clock enters the digest. Original lineage exercise motivated by cross-robot dataset reproducibility. Hashes are caller-supplied commitments, not proof that actual remote bytes match them.

Source: [primary paper](https://arxiv.org/abs/2310.08864). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
