# Solution approach

Validate paired shapes, floating dtype/device, finite nonzero rows and a positive finite scalar temperature. Apply row-wise L2 normalization, matrix-multiply image features by transposed text features, and divide by temperature. Construct torch.arange(B) labels on the logits' device. Average cross_entropy(logits, labels) and cross_entropy(logits.T, labels).

Both calls use mean reduction. Returning the resulting tensor preserves gradients to both inputs. Do not put the calculation inside no_grad.

Time complexity is O(B²D), and the similarity matrix uses O(B²) extra memory. The validation scans O(BD) elements. In a real distributed training loop, the choice of global versus local negatives and differentiable feature gathering must be versioned; this reference is a single-batch component.

Common errors are a missing transpose, softmax before cross-entropy, normalization across samples, swapped target labels, and temperature multiplication where division is required.
