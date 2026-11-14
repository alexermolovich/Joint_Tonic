## Worked examples

**Example 1.** Features `[[1, 0],[-1, 0]]` with epsilon `.01` return distances `[2, 2]`, neighbors `[1, 0]`, and loss `-log(2)`.

**Example 2.** Three identical nonzero feature rows return distances `[0, 0, 0]`, neighbors `[1, 0, 0]`, and loss `-log(epsilon)`. The diagonal is excluded even when other rows are duplicates.
