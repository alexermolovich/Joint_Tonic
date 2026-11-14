# Derive End-to-End Latency from Robotics Trace Events

## Intuition

A pipeline can have several requests in flight. The next output is not necessarily the answer to the earliest input. Correlation IDs preserve which work item crossed the declared boundaries.

## Measure one request's boundary interval

For request i, let $t_i^{\mathrm{in}}$ and $t_i^{\mathrm{out}}$ be its input and output timestamps in integer nanoseconds from one clock. End-to-end latency is

$$
L_i=t_i^{\mathrm{out}}-t_i^{\mathrm{in}}\ge0.
$$

A complete pair is required. Timestamp order in the stored event list does not define association. Intermediate parallel work is outside this two-boundary contract.

## Visual: overlapping requests

| Request | Input ns | Output ns | Latency ns |
|---|---:|---:|---:|
| a | 100 | 160 | 60 |
| b | 110 | 150 | 40 |

Request b finishes before a even though it starts later. Pairing by ID gives the original intervals. This static timeline table is the visual and text alternative.

## Clock and completeness are part of the contract

Subtracting timestamps from unsynchronized clocks mixes elapsed time with clock offset. A missing output can represent loss or incomplete capture; omitting it silently changes the sample. This strict exercise rejects both conditions so callers must resolve them explicitly.

## Why this matters on a robot

Sensor queues, middleware and asynchronous accelerators can reorder completions. A kernel microbenchmark may look fast while the observation-to-command path is late. Boundary measurements capture the declared end-to-end interval, but still depend on accurate instrumentation and a meaningful boundary definition.

## Questions

1. Why not pair each output with the nearest input timestamp?
2. Why is summing all internal stage durations wrong for a parallel graph?

## Sources and prerequisites

RobotPerf motivates explicit workload boundaries and correlated timing. The strict two-event schema is an original bounded trace-analysis exercise, not a complete ROS trace parser or critical-path reconstruction. [Primary source](https://arxiv.org/html/2309.09212v2), SectionIII-D methodology and III-G metrics. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

