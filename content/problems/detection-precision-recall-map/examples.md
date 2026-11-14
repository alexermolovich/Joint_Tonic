# Worked examples

1. One class/two targets in one image. Predictions score0.9 correct targetA,score0.8 duplicateA,score0.7 correctB give precision `[1,0.5,2/3]`,recall `[0.5,0.5,1]`, AP=5/6 via the precision envelope.
2. A class with one target and no predictions has AP0. A second class with no targets has AP NaN and is excluded from mean_ap, so mean_ap=0.
