## Example 1

groups=[[[[1]]],[[[2],[3]]]], present=[[[True]],[[True,False]]] gives tokens=[[[1],[2],[0]]], present=[[True,True,False]], group_ids=[0,1,1], offsets=[0,1,3].

## Example 2

Two empty groups of shape(1,0,2) return tokens(1,0,2), presence(1,0), group_ids(0), offsets=[0,0,0].
