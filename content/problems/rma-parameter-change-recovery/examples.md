## Example 1

Times [0, 1, 2, 3], errors [[2, 0.2, 0.1, 0.1]], all valid, change index 1, tolerance 0.1 and hold length 2 yield recovered true, index 2, delay 1 second, post-change mean 0.4/3 and count 3.

## Example 2

If the record at time 2 is missing, no two consecutive valid samples meet the threshold. Recovery is false, index -1 and delay NaN, even though the final sample is good.
