# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Compute exclusive optical-depth prefixes and stable opacity. Render colors, form the MSE gradient, build suffix color contributions, and apply the analytic density/color derivatives. Use finite differences only as a test oracle.
3. Use the worked trace to check axis order and boundary conventions.
