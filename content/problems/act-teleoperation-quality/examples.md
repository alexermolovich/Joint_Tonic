## Example 1

times=[0,1], joints=[[0],[2]], observed=[True,False], lower=[-1], upper=[1], max_speed=[1] returns missing=[False,True], out_of_range=[False,True], speed_jump=[False,True].

## Example 2

times=[0,0.5], joints=[[0],[1]], both observed, range[-1,1], max_speed=[2] returns all False. Equality at the range and speed thresholds is valid.
