# Hints

## Hint 1

Compute optical thickness first. Its units cancel, which helps catch a missing or double-applied interval length.

## Hint 2

Build an exclusive accumulation: the first prefix is zero, and interval i uses only values before i.

## Hint 3

Use a stable opacity formula, keep the leftover background, and verify the two half-opaque intervals before trying a long ray.
