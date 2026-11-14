# Detect Sensor Timestamp and Calibration Skew

## Intuition

A model can receive the right tensor shape from the wrong exposure time or calibration bundle. Compare these metadata identities before any geometric computation. Keeping the check simple makes its assumptions visible: it verifies a declared pairing, not the truth of a sensor's timestamp.

## Two independent discrepancies

For common sensor s, expected and observed timestamps are $t_s,\hat t_s$ in integer nanoseconds; expected and observed calibration IDs are $c_s,\hat c_s$. With nonnegative timing allowance d,

$$
v_{\mathrm{time}}(s)=\mathbf1[|\hat t_s-t_s|>d],\qquad
v_{\mathrm{cal}}(s)=\mathbf1[\hat c_s\ne c_s].
$$

These predicates are independent. Emit both reasons when both hold. Missing and extra streams are identified from set differences before comparing paired metadata.

Integer subtraction preserves small offsets even when the absolute timestamp is very large. Converting timestamps near $2^{63}$ to floating point first can erase many nanoseconds and falsely accept a mismatch.

## Visual: paired snapshot ledger

| Stream | Time difference | Calibration match | Result |
|---|---:|---|---|
| camera | 11ns | No | calibration; timing |
| joints | 10ns | Yes | Accepted at10ns allowance |

The ledger is a static diagram and its text alternative. Check sensor identity first; comparing wrist time with overhead time is not a valid substitute for a missing wrist observation.

## Why this matters on a robot

A late image paired with current joint positions can move reconstructed geometry even if both arrays are individually valid. Likewise, a replay may silently load a newer camera transform. This task catches declared mismatches; a shared but wrong clock or mislabeled calibration requires additional physical validation.

## Check your understanding

1. Why can one sensor produce two reasons?
2. Does a calibration ID match establish a correct extrinsic transform?

## Sources and prerequisites

The source motivates detecting mismatched data contracts. Timestamp/calibration comparison and the reason codes are original robotics extensions. Matching IDs do not verify the calibration's physical accuracy. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/), Training-serving skew checks, adapted to explicitly declared sensor metadata. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
