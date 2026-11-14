# Associate Map Points with Image Features

Implement `associate_map_features(world_points, map_descriptors, keypoints, image_descriptors, camera_from_world, intrinsics, radius, max_hamming)`.

Associate visible map landmarks with image features using predicted pixels and packed binary descriptors.

`world_points (M,3)` are float64 world meters and `keypoints (F,2)` float64 image `(x,y)` pixels, `0<=M,F<=512`. `map_descriptors (M,32)` and `image_descriptors (F,32)` are actual uint8 arrays: each row stores 256 descriptor bits. This explicitly overrides the ordinary float/index dtype rule for these two arrays. `camera_from_world (4,4)` is a proper float64 rigid transform mapping world to camera, translation in meters. `intrinsics (4,)` is float64 `[fx,fy,cx,cy]` in pixels with focal lengths >=1e-3. Camera axes are x right, y down, z forward. `radius` is a Python int/float in `[0,100]` pixels; `max_hamming` a Python int in `[0,256]`.

Project each landmark only when camera z>1e-6 m. Candidate features have squared pixel distance <=radius squared and bitwise Hamming distance <=max_hamming. Each map point proposes its single best feature by ascending `(Hamming distance, squared pixel distance, feature index)`. Resolve feature collisions by processing those proposals in ascending `(Hamming distance, squared pixel distance, map index)` order, accepting only if the feature is unused. A rejected proposal does NOT retry its second-best feature.

Return int64 `feature_indices (M,)`, int64 `hamming (M,)` and float64 `squared_error (M,)` in a dictionary. Unmatched landmarks have -1 index, -1 Hamming distance and +Inf squared pixel error. Input features are already valid image observations; no image-size, occlusion, octave or orientation filter is implicit. This is an original deterministic pose-guided association policy, not the complete ORB-SLAM2 matcher.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two map points both `[0.,0.,1.]`, zero descriptors, one feature `[0.,0.]` with zero descriptor, identity pose and intrinsics `[1.,1.,0.,0.]`: radius 0, max_hamming 0 gives feature_indices `[0,-1]`. Map-index order breaks the collision.
2. One map descriptor with first byte 255 and remaining bytes 0 versus an all-zero image descriptor differs by 8 bits. With matching pixels, max_hamming 7 rejects it and max_hamming 8 accepts it.

## Source and scope

[Primary source](https://arxiv.org/abs/1610.06475). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
