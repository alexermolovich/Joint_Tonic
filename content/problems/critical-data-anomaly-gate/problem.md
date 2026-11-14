# Block a Pipeline on Critical Data Anomalies

Implement data_anomaly_gate(required_sources, checked_sources, anomalies) -> dict.

required_sources and checked_sources are Python lists of source IDs, each at most10,000 entries. required_sources must be nonempty; duplicates in either list are ignored. IDs and anomaly codes match ASCII [a-z][a-z0-9_-]{0,63}.

anomalies is a Python list of at most50,000 exact three-item tuples (source,code,severity), with severity the string critical or warning. Every anomaly source must occur in checked_sources, although checked sources need not all be required. Identical anomaly tuples are deduplicated. Conflicting severities for the same (source,code) raise ValueError.

Return exactly:
- blocking: sorted unique (source,code) tuples for all critical anomalies.
- warnings: sorted unique (source,code) tuples for all warning anomalies.
- missing_sources: sorted unique required IDs absent from checked_sources.
- blocked: Python bool, true if blocking or missing_sources is nonempty.

A critical anomaly from an additional checked source also blocks; the required list controls minimum coverage, not which supplied critical evidence to ignore. Warnings alone do not block. Empty anomalies is valid; empty checked_sources yields all required IDs missing. Empty required_sources is invalid to avoid accepting a gate with no declared coverage. Every malformed container, identifier, tuple, severity, conflict or unknown anomaly source raises ValueError. Preserve inputs, use no current clock and perform no pipeline side effects.

## Worked examples

### Keep warnings without hiding a critical anomaly

~~~python
data_anomaly_gate(["camera","joints"],["camera","joints"],
                 [("camera","brightness","warning"),("joints","unit","critical")])
# {"blocking":[("joints","unit")],
#  "warnings":[("camera","brightness")],"missing_sources":[],"blocked":True}
~~~

Both sources were checked, but unit evidence blocks the pipeline.

### No anomalies is insufficient without coverage

~~~python
data_anomaly_gate(["joints","camera","camera"],["joints"],[])
# {"blocking":[],"warnings":[],"missing_sources":["camera"],"blocked":True}
~~~

The missing camera validation cannot be inferred to have passed.

## Source and scope

The paper motivates separating validation evidence from downstream pipeline execution. Required-source coverage, severity policy and conflict rules are original teaching choices; a passing data gate is not a robot safety guarantee. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).
