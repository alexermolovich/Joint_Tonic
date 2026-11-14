# Solution

Insert a singleton point axis into the B×G context, broadcast it to B×N×G, and concatenate after the local D channels. Concatenation allocates new storage and preserves empty batches/point sets. This is equivariant to point reordering: local rows move with their duplicated context. Cost and output memory are O(BN(D+G)); no reduction or learned parameters are introduced.
