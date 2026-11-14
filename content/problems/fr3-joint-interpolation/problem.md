# Interpolate Franka FR3 Joint Waypoints

Create the intermediate configurations that move a seven-joint Franka Research 3 arm from a start configuration to a goal configuration.

```python
def interpolate_fr3_joints(q_start, q_goal, num_steps) -> np.ndarray:
    ...
```

`q_start` and `q_goal` are unbatched real array-like vectors with shape `(7,)`, in radians, ordered `fr3_joint1` through `fr3_joint7`. Return a **new float64 array** of shape `(num_steps, 7)` whose rows are evenly spaced in joint coordinates. Include the start in row zero and the goal in the last row. `num_steps` counts samples, not intervals. Do not modify the inputs or return an array sharing their storage.

For sample index $k=0,\ldots,N-1$, where $N=\texttt{num\_steps}$:

$$
\alpha_k=\frac{k}{N-1},\qquad q_k=(1-\alpha_k)q_{\mathrm{start}}+\alpha_kq_{\mathrm{goal}}.
$$

Do not wrap angles: these are bounded joint coordinates, not free circular headings.

## Inputs and errors

- `num_steps`: Python or NumPy integer scalar from **2 through 101**, excluding booleans.
- Joint inputs: finite real integer/floating values. Boolean, complex, string and object array dtypes are invalid. Judge mixed Python sequences by their `np.asarray` dtype, then compute in float64.
- Require exactly `(7,)`; empty arrays, scalars, and batches are invalid.
- Both input vectors must satisfy every inclusive model range below after float64 conversion. Raise **ValueError** for any invalid argument, including failed array conversion. Do not silently clip inputs.

| Joint/column | Minimum (rad) | Maximum (rad) |
|---|---:|---:|
| Joint 1 / 0 | -2.9007 | 2.9007 |
| Joint 2 / 1 | -1.8361 | 1.8361 |
| Joint 3 / 2 | -2.9007 | 2.9007 |
| Joint 4 / 3 | -3.0770 | -0.1169 |
| Joint 5 / 4 | -2.8763 | 2.8763 |
| Joint 6 / 5 | 0.4398 | 4.6216 |
| Joint 7 / 6 | -3.0508 | 3.0508 |

## Try it on the arm

Opening this problem initializes its local **MuJoCo** view. Switch between **Code** and **Simulation** in the right pane. Run your implementation to generate the public demonstration trajectory:

```python
q_start = [0, 0, 0, -1.57079, 0, 1.57079, -0.7853]
q_goal  = [0.4, -0.3, 0.2, -1.8, 0.1, 1.9, -0.4]
num_steps = 41
```

The simulator applies each returned row as joint position and computes forward kinematics. An invalid preview reports an error; it is not replaced by a reference trajectory. Grading uses numerical cases independently of rendering.

The model represents the FR3 arm **without a gripper**. Positive angles follow each joint's local +z axis with the right-hand rule; the scene world/base frame is z-up. The displayed attachment position is in meters. Samples have no timestamps: playback speed is not a commanded robot velocity. This exercise does not test collision clearance, torque limits, inverse kinematics, or real-robot execution safety.

Time and output space: $O(7N)$. See Examples for complete numerical inputs and results.
