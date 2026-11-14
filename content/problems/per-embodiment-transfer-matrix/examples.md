# Worked examples

### Pool counts, not percentages

~~~python
build_transfer_matrix(["solo","mixed"],["arm_a","arm_b"],
 [("mixed","arm_b",1,2),("mixed","arm_b",9,10),("solo","arm_a",2,4)])
# successes = [[2,0],[0,10]]
# trials    = [[4,0],[0,12]]
# observed  = [[True,False],[False,True]]
# rates     = [[0.5,NaN],[NaN,10/12]]
~~~

The mixed-to-arm_b rate is10/12, not the average of0.5 and0.9.

### Preserve axis order and measured failure

~~~python
build_transfer_matrix(["mixed"],["arm_b","arm_a"],[("mixed","arm_a",0,3)])
# successes = [[0,0]]
# trials    = [[0,3]]
# observed  = [[False,True]]
# rates     = [[NaN,0.0]]
~~~

The first target is unmeasured; the second has three measured failures.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

