# Handle the No-Object Class and Padding Masks

Implement build_query_targets(labels, target_valid, matches, num_classes, eos_weight). labels and matches are NumPy int64 arrays; target_valid is NumPy bool. labels/target_valid shape(B,M), matches(B,Q),1<=B<=128,0<=M<=300,1<=Q<=300. num_classes is built-in int excluding bool in[1,1000]. All label entries including padding are in[0,num_classes). matches entries are -1 for unmatched or target indices[0,M); each nonnegative match must refer to a true target_valid slot and may appear at most once per batch. Valid targets need not all be matched. eos_weight is built-in int/float excluding bool in[0,1]. Return new int64 classes(B,Q), defaulting unmatched queries to num_classes (no-object), and float64 weights(B,Q), defaulting unmatched to eos_weight and matched to1. Preserve inputs; noncontiguous supported. TypeError for non-array arguments; ValueError for all other violations. This handles padded target sets and unmatched query supervision; it does not construct image-feature padding masks, solve assignment, or calculate cross-entropy. Indices/weights are dimensionless; each batch is one image exposure.

## Worked examples

## One match and one unused query

labels=[[2,0]], target_valid=[[True,False]], matches=[[0,-1]], num_classes=3,eos_weight=.1. Return classes=[[2,3]], weights=[[1,.1]]. Padding is not a no-object label; it is an unavailable target slot.

## Assignment changes query order

labels=[[1,0]], target_valid=[[True,True]], matches=[[1,-1,0]], num_classes=2,eos_weight=.2. Return classes=[[0,2,1]], weights=[[1,.2,1]]. Ground-truth order is independent of query order.

## Hints

1. Validate all match indices and the target-valid mask before indexing.
2. Initialize query labels to the no-object index.
3. Replace only matched positions; detect duplicate target use per image.
