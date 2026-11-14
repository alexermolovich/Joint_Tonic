# Worked examples

1. Tokens `[[0,0],[0,3],[4,7],[8,11]]`, phrase `[4,11)`, text_length=11 gives `[False,False,True,True]`.
2. Token `[2,5)` overlaps phrase `[4,6)` but not phrase `[5,6)`: touching at a half-open endpoint has zero overlap.
