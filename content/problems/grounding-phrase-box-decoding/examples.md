# Worked examples

1. Box `[0.5,0.5,0.5,1]`, two zero logits, phrase_map=I₂ bool, image (100,200), threshold=0.5 yields query0, phrase0 (tie), score0.5, corners `[50,0,150,100]`.
2. Box `[0,0,1,1]`, one logit0, one phrase, image (10,20), threshold=0.5 yields `[-10,-5,10,5]`. Coordinates remain unclipped.
