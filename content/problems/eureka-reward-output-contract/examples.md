## Example 1

rewards [3], components [[1,2]], valid [True], bound 3, atol 0 -> all flags True, invalid_count 0.

## Example 2

rewards [3,NaN], components [[1,1],[0,0]], valid [True,False], bound 3, atol 0 -> consistent [False,False], accepted [False,False], invalid_count 1.
