# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Take token zero, compute per-row mean and population variance, apply the supplied affine normalization, then matrix-multiply by the head and add its bias.
3. Use the worked trace to check axis order and boundary conventions.
