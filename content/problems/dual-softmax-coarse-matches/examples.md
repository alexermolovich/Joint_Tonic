# Worked examples

1. Two zero source descriptors and two zero target descriptors, D=1, all valid, temperature 1: every confidence is 0.25. At threshold 0, first-index mutual ties retain only `[[0,0]]`; at threshold 0.25 no match survives.
2. Mask the second target in that example: the first column confidence is `[0.5,0.5]` and the second column zero. Only `[[0,0]]` survives at threshold 0.
