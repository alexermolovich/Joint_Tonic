## Example 1

context=[[5]],state=[[2]],IDs=[0],projectors=[[[3]]],context_time=[1],observation_time=[1.2],max_age=.5 returns conditioning[[5,6]],head_ids[0],age[.2],ready[True].

## Example 2

Same features with context_time=[2],observation_time=[1] returns age[-1],ready[False], while keeping conditioning[[5,6]] for inspection.
