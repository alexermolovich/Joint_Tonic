## Example 1

train_ids=[0,0,0], test_ids=[0,1,1], success=[True,True,False], E=2 returns count=[[1,2],[0,0]], rates=[[1,0.5],[NaN,NaN]], same_embodiment_rate=1 and transfer_rate=0.5.

## Example 2

train_ids=[1], test_ids=[1], success=[False], E=2 yields same_embodiment_rate=0 and transfer_rate=None; only cell(1,1) has count1/rate0.
