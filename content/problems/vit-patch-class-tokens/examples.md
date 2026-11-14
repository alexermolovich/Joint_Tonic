# Worked examples

## Two patches

patches=[[[1,2],[3,4]]], projection=[[1,0],[0,2]], bias=[1,-1], cls=[10,20], positions=[[.1,.2],[.3,.4],[.5,.6]], all float64. Output is [[[10.1,20.2],[2.3,3.4],[4.5,7.6]]]. The class token is not sent through the patch projection.

## One feature

patches=[[[2]]], projection=[[3]], bias=[1], cls=[-2], positions=[[.5],[1]], all float32. Output is [[[-1.5],[8]]]. The patch token is 2*3+1+1=8.
