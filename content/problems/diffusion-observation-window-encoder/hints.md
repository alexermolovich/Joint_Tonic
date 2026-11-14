# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Validate aligned shapes and masks, mean-pool spatial image axes, apply the two linear projections and bias, mask invalid slots, and create a separate flattened copy.
3. Use the worked trace to check axis order and boundary conventions.
