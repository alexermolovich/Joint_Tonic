# Map Robot-Specific Data into a Shared Episode Schema

Implement remap_robot_episode(episode: dict, target_channels: list[tuple[str,str]]) -> dict.

episode has exactly values, timestamps_ns, channels, frame, control_mode, dataset_id, dataset_version, robot_id.
- values: finite NumPy float64 array(T,S),0<=T<=10000,1<=S<=64,abs(values)<=1e6.
- timestamps_ns: NumPy int64 array(T,),nonnegative and strictly increasing. Empty is allowed; these are one declared monotonic clock's nanoseconds. No alignment is performed.
- channels: Python list of S tuples(name,unit), with unique names matching ASCII [a-z][a-z0-9_-]{0,63}.
- unit is one of the strings m,cm,mm,rad,deg,unitless.
- frame,dataset_id,dataset_version,robot_id: strings matching the same ASCII identifier rule. Version labels are opaque IDs, not parsed semantic versions.
- control_mode is the string position or delta; it is preserved, never converted.

target_channels is a Python list of1–64 tuples(name,unit), unique names under the same rules. Every target name must occur in source channels; target order defines output order and an arbitrary subset is allowed. A source/target pair must belong to the same unit family: length{m,cm,mm},angle{rad,deg},or unitless{unitless}. Equal names do not permit incompatible family conversions.

Scale factors to family base units are m=1,cm=0.01,mm=0.001,rad=1,deg=pi/180,unitless=1. For each target column compute source_value * source_scale / target_scale using float64. Return a new dictionary with the same exact keys, reordered/converted values(T,D), a copy of timestamps_ns, a new channels list equal to target_channels, and the original metadata strings. Arrays are fresh and independent of inputs and each other; preserve inputs. Noncontiguous arrays are supported.

Every malformed container/field/type/dtype/shape, nonfinite or out-of-range value, nonmonotonic timestamp, duplicate/unknown name or incompatible unit family raises ValueError. Output numerical tolerance is rtol=1e-12,atol=1e-12; metadata/timestamps are exact. No RNG, coordinate transform, kinematics, offset conversion or conversion between position and delta occurs.

## Worked examples

### Reorder and convert a translation

~~~python
episode = {"values":np.array([[90.,25.],[0.,-10.]]),
 "timestamps_ns":np.array([100,200],dtype=np.int64),
 "channels":[("yaw","deg"),("x","cm")],"frame":"base","control_mode":"delta",
 "dataset_id":"set_a","dataset_version":"v1","robot_id":"arm_a"}
out = remap_robot_episode(episode,[("x","m"),("yaw","rad")])
# out["values"] = [[0.25,pi/2],[-0.1,0.0]]
# out["channels"] = [("x","m"),("yaw","rad")]
# timestamps and all five metadata strings are preserved
~~~

This changes units and column order within the same frame. It does not rotate the frame.

### Select one channel while preserving an empty episode

~~~python
episode = {"values":np.empty((0,2)),
 "timestamps_ns":np.empty((0,),dtype=np.int64),
 "channels":[("x","mm"),("grip","unitless")],"frame":"tool","control_mode":"position",
 "dataset_id":"set_b","dataset_version":"v2","robot_id":"gripper_b"}
out = remap_robot_episode(episode,[("grip","unitless")])
# out["values"].shape == (0,1)
# out["timestamps_ns"].shape == (0,)
# out["channels"] == [("grip","unitless")]
~~~

The empty time dimension is retained; channel semantics still exist.

## Source and scope

Open X-Embodiment motivates shared data interfaces that preserve robot-specific meaning. This restricted scalar position/delta mapper and unit table are original teaching choices; they do not reproduce every source dataset transform or make embodiments interchangeable. [Primary source](https://arxiv.org/abs/2310.08864).

