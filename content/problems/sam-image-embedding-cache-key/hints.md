# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Validate all digest strings and the exact shape tuple; serialize the fixed record canonically, hash its ASCII bytes, then compare to the optional cached key.
3. Use the worked trace to check axis order and boundary conventions.
