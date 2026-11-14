# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Validate positive boxes, compute stable paired IoU, apply validity/threshold and phrase equality independently, then aggregate over valid pairs only.
3. Use the worked trace to check axis order and boundary conventions.
