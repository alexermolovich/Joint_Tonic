# Worked differences and boundaries

The complete arrays appear in statement.md.

1. Absolute errors are [[0.125, 0.25], [0.5, 0.125]], so the strict-threshold mask is [[False, True], [True, False]]. Output: [(0, "yaw_rad"), (1, "depth_m")].
2. Errors are [[1, 0.25]] and allowed differences [[1, 0.125]]. Output: [(0, "yaw_rad")].

For an empty batch, use train and serve shape (0,2), names ["depth_m", "yaw_rad"], and atol shape (2,). The result is []. A serve shape (1,2) paired with train shape (0,2) instead raises ValueError.

A shape (3,0) pair, names [], and float64 atol shape (0,) also returns [].

Theory answers: relative tolerance is multiplied by the zero reference; passing paired values does not independently verify schema semantics or correctness. These are public explanatory cases.
