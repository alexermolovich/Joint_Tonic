## Approach

Validate all array shapes, numeric bounds and masks, then apply the stated per-row operation with fresh outputs and explicit missing-support behavior.

Linear in supplied entries, except action support uses O(MND) distance work. Bounded arrays fit the declared CPU budget.
