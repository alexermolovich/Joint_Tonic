# Reference approach

Validate record compatibility and proper rigid matrices. Multiply rotations in frame order; rotate the second translation before adding the first. Invert using the composed rotation transpose and its product with the negative translation. Work and storage are O(1). A point transformed through the original two records must match the composed result and return through the inverse.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
