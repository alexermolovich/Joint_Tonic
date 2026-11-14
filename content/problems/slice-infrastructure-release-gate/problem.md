# Gate a Release on Slice and Infrastructure Tests

Implement:

~~~python
def release_rejections(required: list[str],
                       evidence: dict[str, tuple[str, int, str]],
                       candidate: str, now_ms: int, max_age_ms: int
                       ) -> list[tuple[str, str]]:
    ...
~~~

Check IDs match (slice|infra)/[a-z][a-z0-9_-]{0,63}; names are case-sensitive. required contains 1–10,000 IDs; duplicates are ignored. evidence has at most10,000 entries. Each value is exactly a tuple (tested_version, completed_ms, status), with status pass or fail. Versions match ASCII [a-z][a-z0-9_-]{0,63}. now_ms, max_age_ms and completed_ms are built-in non-bool ints in [0,2**63-1]. Validate every entry, including checks not required.

For each unique required ID, produce at most one rejection by this precedence:

1. No evidence entry: missing.
2. tested_version differs from candidate: wrong_version.
3. completed_ms > now_ms: future.
4. now_ms-completed_ms > max_age_ms: stale.
5. status == "fail": failed.
6. Otherwise no rejection.

Return sorted (check_id,reason) tuples in ascending ASCII check ID order. An empty result means every required check has current passing evidence; it never schedules a deployment. Empty required is invalid, preventing vacuous acceptance. Empty evidence is valid and yields missing for each required ID. Equality at the age bound passes. No mutation.

All input contract violations raise ValueError. A well-typed future timestamp is a rejection reason, not malformed data. There is no implicit wall clock, network, tensor input, physical control command, or random sampling.

## Worked examples

### Explain every failed requirement

~~~python
required = ["slice/night","infra/rollback","infra/runtime","slice/rain"]
evidence = {"slice/night":("v2",900,"pass"),
            "infra/rollback":("v1",990,"pass"),
            "infra/runtime":("v2",950,"fail")}
release_rejections(required,evidence,"v2",1000,100)
# [("infra/rollback","wrong_version"),("infra/runtime","failed"),
#  ("slice/rain","missing")]
~~~

Night evidence is exactly100ms old and passes. The rain slice has no evidence.

### Freshness, future data, and duplicate requirements

~~~python
required = ["slice/fog","infra/timing","slice/fog"]
evidence = {"slice/fog":("v3",99,"pass"),
            "infra/timing":("v3",201,"pass")}
release_rejections(required,evidence,"v3",200,100)
# [("infra/timing","future"),("slice/fog","stale")]
~~~

Fog evidence is101ms old. Duplicating the requirement creates no duplicate result.

## Source and scope

The source motivates testing important slices and ML infrastructure. Version matching, freshness thresholds, reason priority and ID format are original teaching policies; this is an evidence gate, not a complete safety authorization. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
