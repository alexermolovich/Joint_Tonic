# Solution

Validate dictionaries by name, including all tensors before producing output. Iterate in teacher insertion order and compute momentum*teacher+(1-momentum)*student under torch.no_grad(). Each arithmetic expression creates an independent snapshot even at the endpoint momenta; do not return an input directly. The returned parameters are detached and do not mutate either model. Time and output storage are linear in total parameter elements. This is not a complete state_dict update: buffers and optimizer states have separate semantics.
