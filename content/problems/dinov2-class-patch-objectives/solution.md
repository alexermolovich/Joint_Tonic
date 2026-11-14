# Solution

Validate all teacher rows, then detach the supplied targets. Use stable student log-softmax at the supplied temperature. Average class cross-entropy over all images and permitted teacher/student view pairs. Separately average patch cross-entropy over selected positions across the batch. The empty selection contributes student_patch.sum()*0 so backward remains defined. Combine with the supplied weights; no teacher gradients or target renormalization is introduced. Work and storage are O(B(V+P)K).
