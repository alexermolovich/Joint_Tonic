## Example 1

B2,K1 contacts[[[1,0,0]],[[0,1.01,0]]], steps[5,5],max5, state[[2],[3]],initial[[0],[1]],last_action[[.2],[.3]],feet[[.1],[.2]] -> failure[False,True],timeout[False,False],reset[False,True],state[[2],[1]],last_action[[.2],[0]],feet[[.1],[0]],steps[5,0].

## Example 2

zero selected contact bodies, one environment steps6,max5 -> failureFalse,timeoutTrue,resetTrue and the same reset/history-clearing behavior. Timeouts remain separately reported for downstream bootstrap handling.
