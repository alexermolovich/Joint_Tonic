## Example 1

expression "progress - 2 * effort", features progress [3,4], effort [1,.5] -> reward [1,3], used_features ["effort","progress"], node_count 10.

## Example 2

expression "1 + 2", any one valid feature array of length 2 -> reward [3,3], used_features [], node_count 5. Attribute access, calls, division, powers and indexing all raise ValueError.
