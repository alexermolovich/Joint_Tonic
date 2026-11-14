## Example 1

sizes=[2,4], weights=[1,3], uniforms=[[0,0.9],[0.25,0.5]] returns dataset_ids=[0,1], local_indices=[1,2]. The CDF boundary belongs to the next dataset.

## Example 2

sizes=[3,2,5], weights=[0,1,0], uniforms=[[0,0],[0.99,0.99]] returns dataset_ids=[1,1], local_indices=[0,1]. Zero-weight datasets remain unselected.
