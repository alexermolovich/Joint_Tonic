# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
