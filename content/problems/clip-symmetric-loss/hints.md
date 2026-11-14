# Progressive hints

## Hint 1

Pairing is determined by row index. The correct answer for image row `i` is text row `i`, even when the supplied embeddings happen to resemble a different row.

## Hint 2

Normalize each row over the feature dimension, then form a `(B,B)` dot-product matrix and divide by temperature. Cross-entropy expects raw logits, not already softmax-normalized probabilities.

## Hint 3

Compute the mean objective in both retrieval directions with the same diagonal labels, then average them. Retain the tensor and its autograd graph throughout. Positive rescaling of input rows should leave the loss unchanged after normalization.
