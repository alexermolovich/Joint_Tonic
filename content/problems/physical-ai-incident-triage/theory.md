# Triage a Physical-AI Deployment Incident

## Intuition

An incident screen should not let a stream of low-priority errors hide a smaller number of urgent signals. Nor should an old emergency event permanently dominate today's queue. First select a declared observation window, then summarize each component, then order the resulting work queue.

## A window and a reduction

Let n be now_ms and w the nonnegative window width in milliseconds. Event e has timestamp $t_e$, component $c_e$ and numerical severity $p_e\in\{0,1,2\}$. Keep

$$
W=\{e:n-w\le t_e\le n\}.
$$

For each component c with at least one retained event, report

$$
p_c=\min_{e\in W:c_e=c}p_e,\qquad
N_c=|\{e\in W:c_e=c\}|,\qquad
t_c=\min_{e\in W:c_e=c}t_e.
$$

The queue sorts by the tuple $(p_c,t_c,c)$. The last field gives deterministic ordering when severity and first time tie. Counts concern records, not unique physical incidents: without stable event IDs, deduplicating equal tuples would erase potentially distinct observations.

## Visual: filter, group, queue

| Stage for camera in example1 | Remaining records | Result |
|---|---|---|
| Raw stream | 800ms model_error; 920ms sensor_stale | Two records |
| Window [850,1000]ms | 920ms sensor_stale | One retained record |
| Group reduction | priority1, count1, first920ms | camera queue row |

Read downward through the transformations. The table is the static diagram and text alternative. Arm keeps both900ms and950ms records, giving priority0 but first time900ms.

## Why this matters on a robot

A stale camera can cause poor policy decisions even if model inference succeeds. Summaries help engineers correlate sensing, deadlines and execution, but logs may be incomplete or duplicated in transport. Clock offsets can also put valid observations in the future. This task rejects future timestamps rather than inventing a correction. Real incident handling still needs ownership, correlation IDs, raw evidence and hardware procedures.

## Check your understanding

1. Does first_retained_ms mean the time of the most severe event?
2. Why do identical tuples count twice?

## Sources and prerequisites

The paper motivates monitored operational evidence. The event taxonomy, severity mapping and queue ordering are original educational policy; this function summarizes synthetic events and cannot stop, recover or approve a real robot. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/), SectionV: Monitoring tests. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
