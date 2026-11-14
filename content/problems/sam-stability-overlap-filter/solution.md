# Solution

Threshold each logit mask at the base and perturbed levels. Compute high/low count ratios with the declared empty policy and discard empty or unstable base masks before ranking. Sort eligible indices by descending quality and original index, then greedily compare each candidate only with kept binary masks. Suppress strictly above the mask-IoU threshold. This is the specified mask-overlap variant, not SAM box NMS. Worst-case work is O(N²HW), with O(NHW) mask storage.
