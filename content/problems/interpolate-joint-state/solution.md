# Reference approach

Find insertion positions in the sorted source timestamps. Copy exact observations first, then interpolate only bracketed queries whose interval is short enough. Broadcast a single time weight across all joint channels; leave every other row as NaN. Binary search costs O(M log T), validation O(TD), and output/interpolation O(MD); additional output storage is O(MD). Do not clamp out-of-range queries to the first or final sample.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
