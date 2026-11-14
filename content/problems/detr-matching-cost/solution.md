# Solution

Validate all inputs, including an empty target set. Convert center-size boxes to corners only for geometry. Broadcast query and target corners to compute intersection, union, and enclosing areas; GIoU is IoU minus uncovered enclosure fraction. Compute L1 in the original center-size space and index target class probabilities. Combine negative probability, L1, and negative GIoU with the supplied weights. The result is Q×M; the assignment itself is a separate problem. Time and auxiliary memory are O(QM), after validating probabilities.
