## Example 1

rewards=[[1,1]], next_values=[[4,4]], terminated=[[False,True]], both valid, gamma=.5 returns [[3,1]].

## Example 2

A valid truncated transition with reward1, next value4, terminated=False returns3; masking that record invalid returns0.
