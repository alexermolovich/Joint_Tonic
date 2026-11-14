## Example 1

actions=[[[3,9],[5,8]]], available=[[True,False]], mean=[[1,0]], std=[[2,1]] returns normalized=[[[1,0],[2,0]]] and mask=[[[True,False],[True,False]]].

## Example 2

actions=[[[2]],[[2]]], both available, mean=[[0],[2]], std=[[2],[1]] returns normalized=[[[1]],[[0]]]. Equal raw actions need not have equal normalized coordinates across embodiments.
