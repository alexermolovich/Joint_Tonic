# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
