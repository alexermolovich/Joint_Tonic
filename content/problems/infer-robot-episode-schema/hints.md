# Hints

1. Keep one accumulator per signal: metadata, channel extrema and episode occurrence count.

2. Reject width/unit/frame conflicts rather than silently merging them.

3. Allocate independent copies for final minimum and maximum arrays, including one-occurrence signals.
