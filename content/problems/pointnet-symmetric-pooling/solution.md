# Solution

Validate all values, including padding, and require at least one valid point per cloud. Replace invalid slots with negative infinity for the reduction only, then take a maximum along N. Every channel can choose a different winning point. Max is unchanged by reordering its operands, so a joint feature/mask permutation leaves the output invariant. Cost is O(BND) time and up to O(BND) temporary storage.
