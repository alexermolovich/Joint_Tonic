## Example 1

Training=[[0],[100]], actions=[[0],[50],[100]], bins2 returns lower[1], upper[99], codes[[0],[1],[1]], decoded[[25.5],[74.5],[74.5]].

## Example 2

The same training with actions=empty((0,1)) still returns fitted bounds and empty(0,1) codes/decoded; evaluation actions never affect fitting.
