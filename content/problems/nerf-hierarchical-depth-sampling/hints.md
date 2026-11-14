# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Add the mass floor, normalize each ray, build its CDF, then use right-sided interval lookup and linear interpolation for each supplied quantile.
3. Use the worked trace to check axis order and boundary conventions.
