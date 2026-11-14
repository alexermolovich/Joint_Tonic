# Worked examples

1. scores=`[[1,100,3],[4,0,2],[4,9,1]]`, usable=`[True,False,True]`, k=2 gives indices `[1,2]`, scores `[4,4]`. The masked score 100 cannot win.
2. scores=`[[-3,-1],[-2,-4]]`, all tokens usable, k=1 gives index `[0]`, score `[-1]`. Negative logits remain valid evidence.
