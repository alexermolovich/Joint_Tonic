# Hints

1. Check exact shape and dtype before any subtraction; broadcasting can hide a malformed input.
2. Build the allowed difference from the training values, not the serving values. Use strict greater-than for failure.
3. Enumerate mismatches by row then column, and translate column indices using the original name list.

Do not average across features or compare only model predictions. Those answer different questions.
