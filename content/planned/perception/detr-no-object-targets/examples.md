# Worked examples

## One match and one unused query

labels=[[2,0]], target_valid=[[True,False]], matches=[[0,-1]], num_classes=3,eos_weight=.1. Return classes=[[2,3]], weights=[[1,.1]]. Padding is not a no-object label; it is an unavailable target slot.

## Assignment changes query order

labels=[[1,0]], target_valid=[[True,True]], matches=[[1,-1,0]], num_classes=2,eos_weight=.2. Return classes=[[0,2,1]], weights=[[1,.2,1]]. Ground-truth order is independent of query order.
