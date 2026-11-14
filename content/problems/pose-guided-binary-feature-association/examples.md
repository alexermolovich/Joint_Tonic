# Worked examples

1. Two map points both `[0.,0.,1.]`, zero descriptors, one feature `[0.,0.]` with zero descriptor, identity pose and intrinsics `[1.,1.,0.,0.]`: radius 0, max_hamming 0 gives feature_indices `[0,-1]`. Map-index order breaks the collision.
2. One map descriptor with first byte 255 and remaining bytes 0 versus an all-zero image descriptor differs by 8 bits. With matching pixels, max_hamming 7 rejects it and max_hamming 8 accepts it.
