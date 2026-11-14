# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Zero-pad actions, accumulate the three cross-correlation offsets, construct time/context FiLM values, apply stable SiLU and the linear output head.
3. Use the worked trace to check axis order and boundary conventions.
