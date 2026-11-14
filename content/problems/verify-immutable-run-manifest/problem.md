# Reproduce a Model from an Immutable Run Manifest

Implement:

~~~python
def verify_run_manifest(manifest: dict, artifacts: dict[str, bytes],
                        environment: dict[str, str], seed: int
                        ) -> list[tuple[str, str]]:
    ...
~~~

manifest has exactly three keys: artifact_sha256, environment, seed. artifact_sha256 is a dictionary of 1–128 expected artifact names to64-character lowercase hexadecimal SHA-256 digests. environment is a dictionary of 1–32 required runtime/dependency names to version strings. manifest.seed and supplied seed are built-in non-bool ints in [0,2**32-1].

All artifact/environment names match ASCII [a-z][a-z0-9_-]{0,63}. Version values match ASCII [A-Za-z0-9][A-Za-z0-9._+:-]{0,127}. Match versions exactly as opaque strings; no semantic-version ordering, wildcard resolution or package lookup.

artifacts is a dictionary of 0–128 names to built-in bytes, with at most16,777,216 total bytes. Empty payloads are valid. environment is a dictionary of 0–32 observed name/version pairs. Validate every supplied entry, even an unexpected key. None of these inputs is modified.

Compare exact name sets and values. Return one (field,reason) tuple per discrepancy:
- Missing expected artifact: ("artifact/"+name,"missing").
- Unexpected artifact: ("artifact/"+name,"unexpected").
- Present expected artifact whose hashlib.sha256(payload).hexdigest() differs: ("artifact/"+name,"digest_mismatch").
- Missing/extra environment entry: ("environment/"+name,"missing" or "unexpected").
- Present expected environment value differs: ("environment/"+name,"version_mismatch").
- Supplied seed differs from manifest seed: ("seed","mismatch").

Sort by field in ascending ASCII order. Fields are unique, so no secondary reason ordering is needed. Empty results mean supplied inputs match the declared manifest only. Malformed inputs, exceeded bounds and bad digests/types raise ValueError before comparison; mismatches are returned rather than raised. All hashing is over the provided bytes, with no text decoding, files, network, training or randomness.

## Worked examples

### Matching preflight

~~~python
empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
manifest = {"artifact_sha256":{"weights":empty_hash},
            "environment":{"python":"3.12.3"}, "seed":7}
verify_run_manifest(manifest,{"weights":b""},{"python":"3.12.3"},7)
# []
~~~

The empty payload is intentional synthetic data; its SHA-256 matches.

### Separate byte, environment and seed failures

~~~python
manifest = {"artifact_sha256":{"weights":
  "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
  "environment":{"python":"3.12.3"}, "seed":7}
verify_run_manifest(manifest,{"weights":b"x","extra":b""},
                    {"python":"3.11.0"},8)
# [("artifact/extra","unexpected"),("artifact/weights","digest_mismatch"),
#  ("environment/python","version_mismatch"),("seed","mismatch")]
~~~

The extra file is reported even though the expected file is also present. These are valid inputs describing a failed preflight.

## Source and scope

This is a bounded preflight component of model reproduction, motivated by TFX pipeline integration. It validates supplied bytes/versions/seed and deliberately does not run training or promise bitwise-identical weights. The manifest schema and rejection vocabulary are original. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).
