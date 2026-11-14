# Worked examples

## Example 1

Use one-dimensional observations/actions. Online has ID `2`, observation `[0]`, action `[0.2]`, reward `1`, next observation `[1]`, terminated `False`. Demonstration has ID `1`, observation `[3]`, action `[0.1]`, reward `2`, next observation `[4]`, terminated `True`. Output IDs `[1, 2]`, observations `[[3], [0]]`, actions `[[0.1], [0.2]]`, rewards `[2, 1]`, next observations `[[4], [1]]`, terminated `[True, False]` and origin `[2, 1]`.

## Example 2

Place the same transition ID `5` in both sources: observation `[0]`, action `[0.2]`, reward `1`, next observation `[1]`, terminated `False`. The output contains exactly that one row with origin `[3]`. Changing either copy's action to `[0.3]` instead raises `ValueError`.
