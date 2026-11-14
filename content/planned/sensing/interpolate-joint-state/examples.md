# Worked examples

## Camera between encoder samples

Input: times=[0,1,2], q=[[0,2],[1,4],[2,6]], queries=[0.25,1.5], max_gap=1.

Return aligned=[[0.25,2.5],[1.5,5]] and valid=[True,True]. Each joint uses the same time fraction but its own change in angle.

## An exact sample survives a dropout

Input: times=[0,2,5], q=[[0],[2],[8]], queries=[2,3,6], max_gap=2.

Return aligned=[[2],[NaN],[NaN]] and valid=[True,False,False]. The observation at 2 s exists; 3 s lies in a 3 s gap, and 6 s needs extrapolation.
