## Worked examples

1. `initial_position=[0], initial_velocity=[0], targets=[[10],[10],[10]], dt=1, max_velocity=[2], max_acceleration=[1]` → positions `[[1],[3],[5]]`, velocities `[[1],[2],[2]]`.
2. `initial_position=[0], initial_velocity=[2], targets=[[-10]], dt=1, max_velocity=[2], max_acceleration=[1]` → position `[[1]]`, velocity `[[1]]`; braking cannot reverse velocity instantly.
