# Worked examples

### One sensor violates two contracts

~~~python
expected = {"camera":(1000,"cal_v1"),"joints":(1000,"joint_v1")}
observed = {"camera":(1011,"cal_v2"),"joints":(1010,"joint_v1")}
sensor_metadata_skew(expected,observed,10)
# [("camera","calibration"),("camera","timing")]
~~~

Camera is11ns away; joints is exactly10ns away and passes.

### Missing and unexpected streams

~~~python
sensor_metadata_skew({"wrist":(50,"c1")},{"overhead":(50,"c1")},0)
# [("overhead","unexpected"),("wrist","missing")]
~~~

Matching time and calibration labels do not turn a differently named stream into the expected sensor.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
