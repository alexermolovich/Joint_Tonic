# Solution: decode once, emit class records, sort stably

Validate the four-dimensional tensor, positive grid/box dimensions, at least six channels, finite values in `[0,1]`, image dimensions, and score threshold. For each cell/box, compute center and pixel size using the documented row/column axes. Clip corners before deciding whether area is positive.

For every valid box, multiply objectness by each class value and append qualifying records in row/column/box/class order. Python's stable sort with key `-record['score']` preserves this traversal order among tied scores. Use `float(...)` and `int(...)` when constructing records so the interface serializes without NumPy scalar surprises.

No suppression occurs in this stage. A correct decoder must retain two classes for one box if both pass threshold. Likewise, zero score is retained at a zero threshold when the box has positive area; do not use an undocumented positive-score test.

Generation costs O(Sy*Sx*B*C). If D records survive, ordering costs O(D log D) and output storage O(D). Vectorization is possible, but clear bounded loops over the grid are acceptable for this component.
