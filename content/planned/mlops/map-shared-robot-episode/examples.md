# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

