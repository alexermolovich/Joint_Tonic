# Solution

Multiply density by metric length to get dimensionless optical thickness. Use -expm1(-q) for accurate opacity at tiny q. Construct exclusive cumulative thickness by prepending a zero column to the cumulative sum over all earlier intervals; avoid subtracting the current q from an inclusive sum, which loses small previous terms. Exponentiate its negative, multiply by opacity, and return exp(-sum(q)) for background. Do not renormalize or append an opaque last interval. Time and memory are O(RS).
