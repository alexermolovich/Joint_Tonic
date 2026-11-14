# Worked examples

## Centering changes the target

logits=[[2,0],[0,2]], center=[1,0], temperature=1. Output approximately [[0.7310585786,0.2689414214],[0.0474258732,0.9525741268]]. The second row's centered logits are [-1,2].

## Sharpen a fixed margin

logits=[[1,0]], center=[0,0], temperature=.5. Output [[0.8807970780,0.1192029220]]. At temperature1 this would be [0.7310585786,0.2689414214]. Smaller positive temperature concentrates mass on the larger centered score.
