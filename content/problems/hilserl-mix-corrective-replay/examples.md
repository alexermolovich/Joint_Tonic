# Worked examples

## Example 1

Actions `[[0.1], [0.2], [0.3], [0.4]]`, intervention `[True, False, True, False]`, priorities `[0.8, 0.4, 0.1, 0.2]`, batch size `2` and fraction `0.5` produce indices `[2, 3]`, actions `[[0.3], [0.4]]`, intervention `[True, False]` and counts `[1, 1]`.

## Example 2

With the same records, batch size `1` and fraction `0.5`, half-up rounding requests one human row. Return indices `[2]`, actions `[[0.3]]`, intervention `[True]` and counts `[1, 0]`. If no human row exists, raise `ValueError`.
