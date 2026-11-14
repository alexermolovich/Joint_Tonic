# Hints

1. Validate timestamp pairs before sorting; never sort starts and ends independently.
2. Keep duration subtraction in Python integers. For percentage r, the one-based nearest rank is (r*N + 99)//100.
3. Convert the chosen rank to a zero-based list index, then convert the duration to milliseconds. Handle the empty list before indexing.

Do not call a library percentile function without checking its interpolation convention.
