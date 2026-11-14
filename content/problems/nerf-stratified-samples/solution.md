# Solution

Compute one interval width (far-near)/S per ray, add the supplied unit draws to increasing bin indices, multiply by width and shift by near. The result is ordered by construction; no sorting or RNG is needed. Use explicit ray and sample axes to avoid sharing one ray's bounds with another. Time and output storage are O(RS).
