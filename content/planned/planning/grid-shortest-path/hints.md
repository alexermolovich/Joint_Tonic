# Progressive hints

## Hint 1

Treat free cells as graph states. Check map coordinates and endpoint occupancy before beginning search.

## Hint 2

Track best discovered cost separately from priority. Manhattan distance guides expansion but does not replace actual traveled cost.

## Hint 3

Keep predecessors only on strict cost improvement, and follow the declared tie order. Validate the reconstructed path rather than trusting that reaching the goal alone proves it is legal.

