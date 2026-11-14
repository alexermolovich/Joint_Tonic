## Example 1

B=D=1, all four embeddings zero, language logits [0,0,0], valid True, weights [1,1,1,1]: components [log(3),log(3),0,0], loss 2log(3).

## Example 2

all four embeddings [3,4], all language logits zero, weights [0,0,2,3], valid True: components [log(3),log(3),7,5], loss29. With valid False, per_example and all outputs are zero.
