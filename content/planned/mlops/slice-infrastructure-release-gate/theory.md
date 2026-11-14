# Gate a Release on Slice and Infrastructure Tests

## Intuition

A release dashboard can show green checks that belong to yesterday's weights or a different robot. This task asks a narrower question: does every named requirement have passing evidence for this exact version and time window? Scenario checks and infrastructure checks use the same evidence rules.

## Membership, identity, then freshness

Let R be the set of required IDs, v the candidate version, n the current timestamp in integer milliseconds, and a the maximum allowed age. Evidence for i supplies version $v_i$, completion time $t_i$ and status $s_i$. For an existing record, acceptance means

$$
(v_i=v)\land(0\le n-t_i\le a)\land(s_i=\mathrm{pass}).
$$

Release evidence is complete only when every i in R has such a record. The task returns reasons, not a Boolean, so a reviewer can see what to repair. A fixed priority chooses one reason for records with several defects. A wrong-version stale failure reports wrong_version first.

The clock is supplied, making replay deterministic. Subtract integers before comparing; converting large timestamps to floats can lose millisecond differences.

## Visual: evidence decision path

| Condition, in priority order | Result |
|---|---|
| No record | missing |
| Different candidate version | wrong_version |
| Timestamp after now | future |
| Age above limit | stale |
| Failing test | failed |
| All checks satisfied | Omit this ID |

Read top to bottom and stop at the first match. This table is the static diagram and text alternative. In example1, age $1000-900=100$ ms equals the limit, so night passes; runtime has fresh evidence but a failing outcome.

## Why this matters on a robot

Aggregate model accuracy can hide failure in a night-driving or reflective-object slice. Separately, recovery, packaging or timing checks can fail despite a good model. Recording a passing test against the wrong calibration/model bundle defeats both kinds of validation. The caller must choose meaningful IDs and bind version strings to immutable artifacts; this function cannot prove those links.

## Check your understanding

1. Why reject an empty required list?
2. What reason wins for old failing evidence from another version?

## Sources and prerequisites

The source motivates testing important slices and ML infrastructure. Version matching, freshness thresholds, reason priority and ID format are original teaching policies; this is an evidence gate, not a complete safety authorization. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/), Model6: important data slices; Infrastructure tests; SectionV monitoring. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
