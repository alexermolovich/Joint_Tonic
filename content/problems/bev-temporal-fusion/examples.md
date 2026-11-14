# Worked examples

1. current=`[[[2,4]]]`, history=`[[[10,0]]]`, valid=`[[True]]`, gate=`[[0.25]]`, reset=False returns `[[[4,3]]]`.
2. With those same inputs and reset=True, output is `[[[2,4]]]`. An invalid history cell also returns current regardless of its gate.
