## Example 1

datasets=[], schema_version=1 returns canonical_json exactly `{"datasets":[],"schema_version":1}` and sha256 equal to SHA256 of those UTF-8 bytes. Empty manifests are allowed but contain no training data.

## Example 2

A record {"dataset_id":"labA","version":"1.0.0","embodiment":"fr3","content_sha256":"0"*64,"calibration_sha256":"1"*64} is serialized with its keys alphabetically ordered. Reordering its input keys leaves both outputs unchanged; changing version to1.0.1 changes the digest.
