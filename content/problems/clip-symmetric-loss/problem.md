# Compute Symmetric CLIP Contrastive Loss

A robot sees a red cup and receives the instruction “pick up the red cup.” Before generating an action, a vision-language system needs compatible representations of images and instructions. Implement the paired contrastive objective that encourages each image to match its own text while treating other batch entries as negatives.

## Function

~~~python
clip_loss(image_features, text_features, temperature=0.07) -> torch.Tensor
~~~

Both feature tensors have shape **(B, D)** with B ≥ 1 and D ≥ 1. Row i in the image tensor is paired with row i in the text tensor. Inputs must be finite, have nonzero row norms, and share a floating dtype and device. Supported grading dtypes are float32 and float64 on CPU; preserve the device for other valid devices.

Temperature is a finite Python real scalar greater than zero. This API takes the temperature itself, rather than its logarithm or the learned logit scale used in some implementations.

1. Normalize each row independently to unit L2 norm.
2. Form the B×B similarity logits and divide by temperature.
3. Use diagonal indices as the correct class labels.
4. Average mean cross-entropy for image-to-text rows and text-to-image columns.

Return a zero-dimensional tensor with autograd intact. Do not convert the loss to a Python float or detach it. Do not modify either input.

## Examples

**Example 1 — correctly paired orthogonal features**

~~~python
image_features = torch.tensor([[1., 0.], [0., 1.]])
text_features = torch.tensor([[1., 0.], [0., 1.]])
clip_loss(image_features, text_features, temperature=1.)
# tensor(0.3132617...)
~~~

Each correct logit is 1 and its competing logit is 0. Both directions have the same loss log(1 + exp(-1)).

**Example 2 — swapped instructions**

~~~python
text_features = torch.tensor([[0., 1.], [1., 0.]])
clip_loss(image_features, text_features, temperature=1.)
# tensor(1.3132617...)
~~~

The positive target remains the diagonal because pairing is defined by input row order. Swapping the text features should make the objective worse, not silently relabel the pairs.

**Example 3 — a singleton batch**

For any two nonzero one-row feature tensors, the loss is zero: there is only one candidate. This is valid numerically but supplies no contrastive learning signal.

## Constraints and errors

Raise TypeError if either feature input is not a tensor. Raise ValueError for unequal/empty/non-2D shapes, nonfloating or mismatched dtypes/devices, nonfinite values, zero-norm rows, or an invalid temperature (including bool). No distributed gathering, encoder model, image preprocessing, or random sampling is required. Time is O(B²D), with O(B²) logits.

## Hints

- Normalize along the feature axis, not across the batch.
- Cross-entropy accepts logits directly; computing softmax first is unnecessary.
- The second direction uses the transposed logits and the same labels.

Source: [CLIP paper](https://arxiv.org/abs/2103.00020). This exercise isolates the paired objective with supplied embeddings.
