## Example 1

action_error=[[1],[1],[1]], chunk_lengths=[1,2,3] returns [1,2,14/3]. The last length2 chunk contains only the final sample.

## Example 2

action_error=[[1],[-1]], chunk_lengths=[2,1] returns [0.5,1]. Cancellation can make a longer chunk score lower in this toy diagnostic.
