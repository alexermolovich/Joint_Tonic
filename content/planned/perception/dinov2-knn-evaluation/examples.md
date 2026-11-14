# Worked examples

## Closest prototype

train=[[1,0],[0,1],[-1,0]], labels=[0,1,1], queries=[[1,0],[0,1]], k=1,num_classes=2,temperature=1. Return predictions=[0,1], scores=[[1,0],[0,1]].

## Weighted vote

train=[[1,0],[0,1]], labels=[0,1], queries=[[1,0]], k=2,num_classes=2,temperature=1. Selected similarities[1,0] give scores=[[.7310585786,.2689414214]], prediction=[0].
