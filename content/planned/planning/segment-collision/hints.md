# Progressive hints

## Hint 1

Represent every candidate location with one parameter t between zero and one.

## Hint 2

Each coordinate gives an interval of t values that lie inside the obstacle slab. Intersect those intervals rather than sampling the path.

## Hint 3

Handle parallel axes without division, treat interval equality as contact, and compare entry times across all obstacles before selecting the first hit.

