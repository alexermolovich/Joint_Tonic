# Worked examples

## Example 1

Both policies have two valid autonomous trials. Success is `[[True, False], [True, True]]`, with no violations or assistance. Versions `1` and `2`, minimum trials `2`, allowed drop `0` and maximum violation rate `0` produce counts `[2, 2]`, success_rate `[0.5, 1]`, violation_rate `[0, 0]`, checks `[True, True, True, True]` and accepted `True`.

## Example 2

Mark both candidate trials in Example 1 as assisted. Return counts `[2, 0]`, success_rate `[0.5, NaN]`, violation_rate `[0, NaN]`, checks `[True, False, False, False]` and accepted `False`.
