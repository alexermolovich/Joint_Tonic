# Solution

Treat targets as rows and queries as columns. Maintain target/query potentials, per-column slack and predecessor columns; each new target augments the current matching through an alternating path. Potential updates expose a free query without freezing earlier assignments. Return the matched query for each target, preserving target order. The rectangular algorithm takes O(M²Q) time and O(M+Q) auxiliary storage beyond the cost array. Any tied optimum is acceptable; greedy assignment is not.
