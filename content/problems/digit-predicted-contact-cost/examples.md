## Example 1

Two single-pixel predictions 0 and 1, goal 0, efforts [1, 0], weight 0.2 and both candidates valid yield image errors [0, 1], costs [0.2, 1] and best index 0.

## Example 2

Two identical zero-error predictions with zero effort choose index 0. If both candidates are invalid, costs are NaN and best index is -1.
