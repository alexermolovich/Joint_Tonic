# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Validate the common grid; use the validity mask before reshaping both arrays. Broadcast positions across batches, build row/column coordinates, and copy outputs so they share no storage with inputs or one another.
3. Use the worked trace to check axis order and boundary conventions.
