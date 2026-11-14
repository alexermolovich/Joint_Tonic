## Approach

Validate aligned widths and source bounds, then gather each requested source row and record its modality. Allocate explicit empty output shape when L is zero.

O(L*E + total source entries) time for validation/gather and O(L*E) output.
