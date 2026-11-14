# Progressive hints

## Hint 1

Form the residual before reduction, expand valid with a final singleton channel axis, and exclude padded vectors.

## Hint 2

Count valid horizon entries, then multiply by prediction.shape[-1]. Check all-padding before dividing.

## Hint 3

Keep the result as a tensor. Calling.item() or constructing a new tensor from the numeric value discards the gradient graph.
