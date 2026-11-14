## Example 1

present=[[True,True]], timestamps=[[9,8]], now=[10], max_age=[1,1], required=[True,True] returns usable=[[True,False]], stale=[[False,True]], ready=[False].

## Example 2

present=[[False,True]], timestamps=[[0,11]], now=[10], max_age=[1,1], required=[False,False] returns usable=[[False,False]], stale=[[False,True]], ready=[True]. No required sensors is a deliberate vacuous gate, not proof of useful perception.
