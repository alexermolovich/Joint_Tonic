# Worked examples

## Example 1

With new transitions `[2, 0, 1]`, warmup `0`, ratio `2/1`, cap `3` and publication interval `2`, return updates `[3, 1, 2]`, completed `[3, 4, 6]`, backlog `[1, 0, 0]`, published_version `[3, 4, 6]` and publish `[True, True, True]`.

## Example 2

With new transitions `[2, 1]`, warmup `2`, ratio `1/2`, cap `10` and publication interval `2`, the floored targets are `[0, 0]`. All four integer outputs are `[0, 0]`, and publish is `[False, False]`.
