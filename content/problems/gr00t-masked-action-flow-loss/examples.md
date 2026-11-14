## Example 1

prediction=[[[0,9]]],clean=[[[3,7]]],noise=[[[1,2]]],valid=[[[True,False]]] gives target[2,5], loss4,per_example[4],gradient[[[-4,0]]].

## Example 2

With all-False mask, even nonzero prediction errors produce loss0,per_example[0],gradient all0; they are unsupported labels, not negative examples.
