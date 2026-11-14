# PR draft: Make evaluator provenance reproducible across checkouts

Related local issue: `docs/issues/cross-platform-evaluator-hashes.md`. This draft has not been posted to GitHub; authenticated remote issue/PR access is unavailable.

Windows CRLF evaluator files produced 105 declared hashes that disagreed with the LF files shipped by Git. Raw source-manifest hashing also made equivalent catalog plans depend on checkout line endings. This change establishes LF source attributes, repairs those metadata hashes and 58 corresponding blueprint hashes, and hashes canonical UTF-8 text while preserving binary bytes.

Catalog preparation now rejects non-LF evaluator bytes and stale declared hashes, keeping raw worker lineage consistent with the catalog. Existing immutable-version checks and real-image requirements remain intact. No hosted database operation or learner-contract change is included.

Validation: four focused tests cover LF/CRLF equivalence, lone-CR normalization, UTF-8/BOM/newline preservation, binary identity, actual source changes, minimal metadata/blueprint repair and all 274 checkpoint packages. All declared hashes match after repair; 22 legacy packages have no declared hash and continue to use runtime-derived lineage. Content/schema validation passes. No `cases.py` or reference-code semantic diff is present, and no unchanged numerical evaluator was rerun.

Main-worker review and merge are still required. The final commit and exact diff are supplied in the agent handoff; this document makes no claim of a remote PR or merge.
