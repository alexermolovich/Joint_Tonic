# Worked examples

## Example 1

For probabilities `[0.9, 0.8, 0.2]`, success labels `[True, False, False]`, failure types `[-1, 0, 1]`, all valid, threshold `0.5` and two failure types, return confusion `[1, 1, 0, 1]`, precision `0.5`, recall `1.0`, failure counts `[1, 1]`, false-positive counts `[1, 0]` and rates `[1.0, 0.0]`.

## Example 2

One failure of type 0 has probability `0.5`. With threshold `0.5` and two failure types, it is a false positive: confusion `[0, 1, 0, 0]`, precision `0`, recall `NaN`, failure counts `[1, 0]`, false-positive counts `[1, 0]` and rates `[1, NaN]`.
