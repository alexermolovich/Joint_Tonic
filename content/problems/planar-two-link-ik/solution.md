# Reference approach

Validate lengths and their ratio, then test the reachable annulus. Handle the equal-length origin convention. Clamp the elbow cosine only after reachability, select arccos for the positive branch, subtract the internal offset from the target bearing, and normalize the shoulder angle. Work and storage are O(1). Check the returned angles with independent forward kinematics; this does not enforce collisions, limits or continuity.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
