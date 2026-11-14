# Version a Cross-Robot Dataset Manifest

A mixed dataset needs an identity that includes its versions, embodiments and calibration. Canonical serialization avoids treating harmless dictionary ordering as a new experiment while detecting changes that affect interpretation.

## Contract

`version_dataset_manifest(datasets,schema_version)` takes a Python list of0..128 records and a built-in integer schema_version1..1000, excluding bool. Each record is a dict with exactly dataset_id, version, embodiment, content_sha256, calibration_sha256. dataset_id and embodiment match [A-Za-z][A-Za-z0-9_-]{0,31}; version matches nonnegative decimal major.minor.patch with no leading zeros except0, each component<=9999; hashes are64 lowercase hexadecimal characters. IDs must be unique. Sort records by dataset_id, construct payload={"schema_version":schema_version,"datasets":sorted_records}, and serialize with json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=True). Return {"canonical_json":str,"sha256":lowercase SHA256 of its UTF-8 bytes}. Input dict/list order must not change the digest; any content/calibration/version change must. Do not read external files or fetch URLs.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Registry IDs, semantic versions and byte-content hashes have no physical units; calibration hashes identify externally pinned physical conventions. An immutable snapshot, not a mutable latest-version pointer; no wall clock enters the digest. Original lineage exercise motivated by cross-robot dataset reproducibility. Hashes are caller-supplied commitments, not proof that actual remote bytes match them.


## Example 1

datasets=[], schema_version=1 returns canonical_json exactly `{"datasets":[],"schema_version":1}` and sha256 equal to SHA256 of those UTF-8 bytes. Empty manifests are allowed but contain no training data.

## Example 2

A record {"dataset_id":"labA","version":"1.0.0","embodiment":"fr3","content_sha256":"0"*64,"calibration_sha256":"1"*64} is serialized with its keys alphabetically ordered. Reordering its input keys leaves both outputs unchanged; changing version to1.0.1 changes the digest.
