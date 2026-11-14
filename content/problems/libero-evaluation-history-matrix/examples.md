# Worked examples

### Example 1

task_order=[a,b],events e1(stage0,b,False),e2(stage1,a,True),e2 repeated -> counts[[0,1],[1,0],[0,0]],successes[[0,0],[1,0],[0,0]],rates[[NaN,0],[1,NaN],[NaN,NaN]].

### Example 2

task_order=[a], events e1(stage1,a,True),e2(stage1,a,False) -> counts[[0],[2]],successes[[0],[1]],rates[[NaN],[0.5]].
