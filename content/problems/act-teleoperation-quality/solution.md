## Approach

Validate axis alignment, compare joint positions to bounds, compute adjacent dt-normalized changes, then reduce each row across joints.

O(T*D) time and output/working storage.
