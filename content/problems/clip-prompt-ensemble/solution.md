# Solution

Validate each image and prompt norm. Normalize prompts independently along D, average them only within their class, reject a nearly cancelling class mean, and normalize the mean again. Normalize image rows and compute their dot products with class prototypes divided by positive temperature. Returning logits preserves score ordering without an unnecessary softmax. Prototype construction costs O(CPD), and scoring costs O(BCD).
