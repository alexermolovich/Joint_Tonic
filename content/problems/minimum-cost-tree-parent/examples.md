# Worked examples

1. Root costs `[3.,1.,2.]`, edge costs `[1.,4.,2.]`, all feasible gives totals `[4.,5.,4.]`: parent0 and total_cost4, using the lower index for a tie.
2. Root costs `[0.,5.]`, edge costs `[0.,1.]`, feasible `[False,False]` returns parent -1 and total_cost +infinity. An infeasible cheap connection cannot become a parent.
