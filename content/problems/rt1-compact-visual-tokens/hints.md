# Progressive hints

## Hint 1

Each (batch, output-token) row is a separate distribution over spatial locations. Broadcast valid from(B,N) to(B,1,N).

## Hint 2

Mask before softmax and normalize the last logits axis. Keep the original features for the weighted sum; normalized logits are not new features.

## Hint 3

Contract shapes are weights(B,K,N) times features(B,N,C). Check the masked third location and the independent one-location batches before checking gradients.
