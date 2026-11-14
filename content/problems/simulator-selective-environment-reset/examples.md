# Worked examples

### Example 1

state=[[1,2],[3,4]],reset_state=[[0,0],[9,9]],done=[True,False],episode_ids=[4,8],steps=[10,20] -> state[[0,0],[3,4]],episode_ids[5,8],steps[0,20].

### Example 2

done=[False],episode_ids=[2^63-1],steps=[7] preserves both counters and the original state row.
