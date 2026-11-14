## Worked examples

**Example 1.** For a one-row grid, features are `[2, 4]`, positions `[10, 20]` and validity `[True, False]`, each with one channel. Output tokens `[2, 0]`, positional tokens `[10, 0]`, padding `[False, True]`, coordinates `[[0, 0],[0, 1]]` (batch/channel dimensions retained).

**Example 2.** Mark both pixels invalid. Output content and positional arrays are zero, padding is `[True, True]`, and coordinates remain `[[0, 0],[0, 1]]`.
