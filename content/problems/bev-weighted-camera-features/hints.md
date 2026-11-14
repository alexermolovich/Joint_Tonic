# Hints

1. Apply the mask to weights before both sums.
2. Reduce camera and sample axes, preserving batch/query/channel axes.
3. Divide only rows with positive mass and return an explicit observed mask.
