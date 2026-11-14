# Worked examples

1. accuracy=`[0.7,0.8,0.75]`, latency=`[10,20,25]` ms, budget=20: frontier `[0,1]`, selected 1. Candidate 2 is both slower and less accurate than 1.
2. accuracy=`[0.8,0.8]`, latency=`[20,20]`, budget=19: frontier `[0,1]`, selected -1. Identical measurements do not dominate each other; both miss the deadline.
