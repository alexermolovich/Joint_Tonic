## Approach

Validate common batch/channel axes and positive scales, broadcast across H, calculate standardized coordinates and zero only unavailable entries.

O(B*H*D) time and output memory.
