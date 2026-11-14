## Example 1

valid=[True,False], success=[True,True], slice_ids=[0,0], num_slices=2 returns count=[2,0], invalid_rate=[0.5,NaN], success_rate=[0.5,NaN]. The invalid row is not a success.

## Example 2

valid=[True,True], success=[False,True], slice_ids=[1,0], num_slices=2 returns count=[1,1], invalid_rate=[0,0], success_rate=[1,0]. Output order is slice-ID order.
