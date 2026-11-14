# Worked outputs and boundary cases

The complete inputs appear in statement.md.

| Example | Reached, including roots | Output |
|---|---|---|
| Calibration | calib, features, policy, monitor | ["features", "monitor", "policy"] |
| Feedback | policy, log, data, dashboard | ["dashboard", "data", "log"] |

~~~python
blast_radius([], [], [])  # []
blast_radius(["camera"], [("camera", "camera")], ["camera"])  # []
blast_radius(["camera"], [], ["unknown"])  # ValueError
~~~

Question 1 answer: ["dashboard", "log"]. Question 2: undeclared consumers are absent from the graph and cannot be inferred from these inputs. These are explanatory fixtures, not hidden tests.
