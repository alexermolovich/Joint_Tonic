# Reference approach

Scale each nonzero quaternion by its largest absolute component and normalize. Combine scalar and vector parts with the Hamilton dot/cross-product rule, then normalize the result. Work and storage are O(1). Do not change the sign or reverse the inputs: the independently composed rotation matrices must agree.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
