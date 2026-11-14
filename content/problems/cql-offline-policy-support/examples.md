## Example 1

Logged states [0, 0] with actions [[0], [1]] and query state [0] with action [[0.5]] produce nearest index [0] and distance [0.5]. At threshold 0.5, unsupported is false; equal-distance ties choose the first row.

## Example 2

The same query action at state 1 has no matching logged state: nearest index [-1], distance [NaN] and unsupported [True].
