## Example 1

Action times [0, 1], commands [[0.2], [0.8]], frame times [0.5, 1] and max_age 0.5 yield indices [0, 1], ages [0.5, 0], both valid, and aligned commands [[0.2], [0.8]].

## Example 2

With one action at time 1 and frames at [0.5, 2], max_age 0.5 yields indices [-1, 0], ages [NaN, 1], both invalid, and zero aligned commands.
