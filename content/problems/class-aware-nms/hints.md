# Progressive hints

## Hint 1

Keep original indices as the working candidate list. Sort by confidence once; resolve ties using the original index. The returned indices must still refer to the caller's arrays.

## Hint 2

After choosing the first remaining box, calculate its IoU against the rest. Remove a candidate only when both its class matches and IoU is strictly greater than the threshold.

## Hint 3

A removed candidate never gets a turn to suppress others. Filter the working list before the next iteration. Preserve candidates with equal-threshold overlap, different classes, or zero intersection—even if their coordinates look nearly identical.
