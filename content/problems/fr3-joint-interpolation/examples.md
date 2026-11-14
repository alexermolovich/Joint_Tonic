## Example 1: one midpoint

```python
q_start = [0, 0, 0, -1, 0, 1, 0]
q_goal  = [0.4, 0.2, -0.2, -1.4, 0.6, 1.4, -0.4]
num_steps = 3
```

Output (float64):

```python
[[0.0, 0.0,  0.0, -1.0, 0.0, 1.0,  0.0],
 [0.2, 0.1, -0.1, -1.2, 0.3, 1.2, -0.2],
 [0.4, 0.2, -0.2, -1.4, 0.6, 1.4, -0.4]]
```

Three samples create **two intervals**. Joint 4 decreases by 0.2 radians per interval while joint 6 increases by 0.2 radians. All joints share the same interpolation fraction.

## Example 2: stationary arm

```python
q_start = [0, 0, 0, -1, 0, 1, 0]
q_goal  = [0, 0, 0, -1, 0, 1, 0]
num_steps = 4
```

Output:

```python
[[0., 0., 0., -1., 0., 1., 0.],
 [0., 0., 0., -1., 0., 1., 0.],
 [0., 0., 0., -1., 0., 1., 0.],
 [0., 0., 0., -1., 0., 1., 0.]]
```

Zero displacement still produces the requested number of rows. It is not an empty trajectory.

## Example 3: endpoints only

With the inputs of Example 1 and `num_steps=2`, the output contains exactly `q_start` and `q_goal`. There is no interior sample.
