# Extract a Depth, Width, and Kernel Subnetwork

Implement extract_subnetwork(weights, depth, width, kernel) -> list[np.ndarray].

weights is a list of1–16 NumPy float64 arrays, all finite and same shape(C,C,K,K), 1<=C<=64, odd1<=K<=9, absolute values<=100, total input entries<=1000000. These are consecutive SAME-width convolution blocks after a caller-provided compatible stem. depth,width,kernel are built-in non-bool ints, 1<=depth<=len(weights),1<=width<=C, and positive odd kernel<=K. Noncontiguous arrays are valid.

Return fresh independent arrays for the first depth blocks: select the FIRST width output and input channels, and the centered spatial kernel crop. Each output has shape(width,width,kernel,kernel). Preserve inputs and do not alias between output layers, even if input arrays alias. Validate every input layer, including layers beyond depth. Invalid types, dimensions, values or budgets raise ValueError.

Kernel center cropping is an ORIGINAL teaching simplification, not Once-for-All's learned kernel transformations. There are no activations, BN statistics, shortcuts, width sorting, training or inference. The caller must provide a stem and head matching the selected width; this is a block-parameter extraction task, not a complete executable model.

## Worked examples

### Center crop
For `weights=[np.arange(9,dtype=np.float64).reshape(1,1,3,3)]`, depth1,width1,kernel1 returns `[np.array([[[[4.]]]])]`.

### Depth and width both shrink
For two layers filled with2 and3 respectively, each shape(2,2,3,3), depth1,width1,kernel3 returns one independent array of shape(1,1,3,3) filled with2.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
