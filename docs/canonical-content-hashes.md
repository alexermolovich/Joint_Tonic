# Canonical source and evaluator hashes

Versioned source text uses UTF-8 and LF line endings. `.gitattributes` makes fresh Windows and Linux checkouts agree while preserving binary assets. Existing working files may retain old line endings until they are normalized.

Before building an evaluator image or planning a catalog release, run:

```powershell
node scripts/check-evaluator-hashes.mjs
```

If the check reports line endings or stale declared hashes, review and apply the narrow repair:

```powershell
node scripts/check-evaluator-hashes.mjs --write
node scripts/check-evaluator-hashes.mjs
node --test tests/canonical-source.test.mjs
```

The repair converts evaluator line endings to LF and updates existing `grading.evaluator_sha256` values in metadata and blueprint front matter. It preserves numerical formatting, problem versions, tests and learner contracts. Older packages without a declared hash remain explicitly counted as undeclared; runtime and catalog lineage still derive their hash from actual evaluator bytes. No source code is executed by this check.

Catalog source identities normalize recognized UTF-8 source-text formats before hashing their sorted file manifest. Binary and unknown formats remain byte-exact. Unicode content, byte-order marks and the presence of a final newline remain significant. Real content changes still change the identity; platform line endings do not.

The actual worker hashes raw `cases.py` bytes. Catalog planning therefore rejects a noncanonical evaluator or stale declared hash before writing a plan or contacting Supabase. Normalize source before building the image, and supply only its actual immutable digest. Canonical content hashing does not prove that an image contains the expected files; runtime qualification must still verify that identity.

This fix performs no hosted writes and does not alter existing immutable catalog conflict handling. If a remote version already has a different identity, publication remains blocked until its version/provenance transition is reviewed. No numerical test rerun is needed solely for an unchanged evaluator's newline normalization; changed evaluator logic still requires its ordinary sandbox checks.
