# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Validate shapes and ranges, compute a stable full softmax, choose foreground argmax, convert box corners, then apply one common validity mask to every output.
3. Use the worked trace to check axis order and boundary conventions.
