# Detect Sensor Timestamp and Calibration Skew

Implement sensor_metadata_skew(expected, observed, max_delta_ns) -> list[tuple[str,str]].

expected and observed are Python dictionaries of at most1,000 sensor IDs to exact two-item tuples (timestamp_ns, calibration_id). Sensor and calibration IDs match ASCII [a-z][a-z0-9_-]{0,63}. Times and max_delta_ns are built-in non-bool integers in [0,2**63-1]. Validate every entry; malformed inputs raise ValueError.

Compare the union of sensors:
- In expected only: (sensor,"missing").
- In observed only: (sensor,"unexpected").
- In both, differing calibration IDs: (sensor,"calibration").
- In both, abs(observed_time-expected_time)>max_delta_ns: (sensor,"timing").

Common sensors can produce both calibration and timing. Return tuples sorted by (sensor,reason), ASCII order; calibration precedes timing for the same sensor. Equality at the timing bound passes. Two empty snapshots return []; missing/extra sensors are outcomes rather than exceptions. All time arithmetic stays integer; preserve inputs.

Calibration IDs are opaque immutable bundle identities, not matrices to estimate or compare numerically. A common synchronized clock and intended observation pairing are assumptions. No interpolation, clock correction, sensor I/O or hidden current time.

## Worked examples

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

## Source and scope

The source motivates detecting mismatched data contracts. Timestamp/calibration comparison and the reason codes are original robotics extensions. Matching IDs do not verify the calibration's physical accuracy. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).
