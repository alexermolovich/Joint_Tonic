## Example 1

One RGB frame [128, 128, 128] of size 1 by 1, timestamp 0, ID 0, exposure 1000 and expected exposure 1000 yields no flags, usable [True], saturation fraction [0] and ready True.

## Example 2

Two normal frames at times [0, 0.2], IDs [0, 2] and max_gap 0.1 produce timing and ID flags on the second frame. If that frame contains only 255, its saturation flag is also true.
