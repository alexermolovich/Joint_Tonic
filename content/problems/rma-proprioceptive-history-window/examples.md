## Example 1

Observations [[1], [2], [3]], actions [[0.1], [0.2], [0.3]], episode IDs [0, 0, 0], query [2] and H=3 produce history [[[0, 0], [1, 0.1], [2, 0.2]]], validity [[False, True, True]] and indices [[-1, 0, 1]].

## Example 2

Changing episode IDs to [0, 0, 1] makes query 2 the first row of a new episode. Its previous-history window is entirely padded.
