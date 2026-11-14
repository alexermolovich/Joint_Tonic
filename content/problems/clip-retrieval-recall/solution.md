# Solution

Use stable descending sorting along rows for image queries and columns for text queries. Original candidate order gives the lower-index tie rule. For each query test whether its diagonal positive appears in the first k indices, then average those Boolean hits. The two means are separate because ranking across the two axes can differ. Sorting costs O(N² log N) time and O(N²) space. No softmax or score calibration is needed.
