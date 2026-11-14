# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Build the in-bounds mask, replace unused coordinates before indexing, gather four camera-specific neighbors and blend with fractional offsets. Zero all unused output vectors.
3. Use the worked trace to check axis order and boundary conventions.
