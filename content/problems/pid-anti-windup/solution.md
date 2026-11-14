# Reference approach

Calculate the derivative and candidate integral. Inspect the candidate effort together with the sign of the error; only reject integration that pushes farther into saturation. Recompute effort from the chosen integral, then clip. This uses O(1) time and space. A saturated command with error pointing inward must still unwind the integral.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
