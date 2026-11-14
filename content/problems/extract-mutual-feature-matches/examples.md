# Worked examples

1. Assignment `[[0.8,0.1,0.],[0.2,0.7,0.],[0.,0.,0.]]`, threshold 0.5: pairs `[[0,0],[1,1]]`, source and target matches `[0,1]`, confidence `[0.8,0.7]`.
2. An all-ones real `2x2` block with threshold 0 has only pair `[[0,0]]`: first-index argmax ties must be reciprocal. With threshold 1 no pair passes the strict comparison.
