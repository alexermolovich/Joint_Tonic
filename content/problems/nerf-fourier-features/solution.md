# Solution

Construct increasing frequencies 2^ell*pi. Multiplying positions with a separate level axis produces N×L×3 phases. Concatenate sine and cosine along the last axis and flatten the last two axes, yielding level-major channel order. Explicit dimensions preserve N=0 and L=0. Complexity and storage are O(NL). Small roundoff near trigonometric zeros is expected.
