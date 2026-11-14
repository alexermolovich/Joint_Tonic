# Worked examples

## Execute only a near-term segment

trajectory=[[[10],[20],[30],[40]]], valid=[[True,True,True,True]], offset=1, execute_steps=2.

Return [[[20],[30]]]. The next observation may replace the rest of the plan; the final40 is not queued by this call.

## Padding outside the selected window

trajectory=[[[1,2],[3,4],[0,0]]], valid=[[True,True,False]], offset=0, execute_steps=2.

Return [[[1,2],[3,4]]]. Asking instead for offset=1,execute_steps=2 raises ValueError, because the selected tail includes unavailable target data.
