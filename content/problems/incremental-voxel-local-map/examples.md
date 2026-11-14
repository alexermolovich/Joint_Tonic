# Worked examples

1. Existing points [[0.1,0,0],[0.4,0,0]], incoming [[0.6,0,0]], identity pose, center [0,0,0], half extents [2,2,2] and voxel size 1 select existing index 1. Points 0.4 and 0.6 tie around center 0.5, so the earlier candidate wins. Removed-existing flags are [True,False].
2. Existing [-0.1,0,0] and incoming [0,0,0] belong to voxel keys [-1,0,0] and [0,0,0]. Negative coordinates use floor, not truncation toward zero.
