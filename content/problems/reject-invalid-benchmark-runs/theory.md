# Reject Invalid Benchmark Runs

## Intuition

A benchmark number is credible only with its workload identity and complete evidence. Dropping failed or unfinished requests can make a system look fast. Detect those omissions before comparing performance summaries.

## Account for every requested query

Let E be expected queries, C successfully completed and F failed. Require $C,F,E\ge0$ and

$$
C+F\le E,\qquad U=E-C-F.
$$

U is unfinished work, not a successful query. Gate validity requires $U=0$ and $F=0$, plus supplied minimum completed count, duration and quality:

$$
C\ge C_{\min},\qquad D\ge D_{\min},\qquad Q\ge Q_{\min}.
$$

D is integer nanoseconds over the declared interval; Q is the same dimensionless metric in both run and protocol. Scenario and model identity are exact labels. These equations define this teaching validator, not all rules of a benchmark release.

## Visual: distinguish missing work from failures

| Expected | Completed | Failed | Unfinished | Meaning |
|---:|---:|---:|---:|---|
| 10 | 10 | 0 | 0 | Complete accounting without failures |
| 10 | 8 | 1 | 1 | One failure and one missing completion |

The second row triggers both failed_queries and incomplete. The original table is the visual and text alternative.

## Why multiple reasons matter

Reporting only the first failure can hide a quality regression behind a short duration. Returning every independent reason gives the learner a complete explanation. Malformed evidence is different: impossible counts are rejected as an invalid input contract before a gate decision.

## Why this matters on a robot

The slowest or failed frames may be exactly the observations needed for a control deadline. Removing them biases a benchmark toward easy cases. Device/model/scenario identity must remain attached so two reports represent comparable workloads.

## Questions

1. Why is C+F>E an error rather than another rejection reason?
2. Does a matching model hash establish that the supplied evidence was honestly measured?

## Sources and prerequisites

MLPerf motivates comparable workloads and valid quality-constrained measurements. This small evidence validator and its supplied thresholds are original; it is not an official MLPerf submission, statistical confidence or audit checker. [Primary source](https://arxiv.org/html/1911.02549v1), Sections4.4,4.6,4.7 and5: quality, validity and review; supplied thresholds are original. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

