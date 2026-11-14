# Worked examples

1. Points `[[0,0,0],[50,0,0],[100,0,0]]`, unit="cm", matching frame="base", voxel_size=1 m occupy 2 voxels, density 1.5 points/voxel, extent `[1,0,0]` m.
2. Points `[[-0.01,0,0],[0,0,0]]` in meters with voxel_size=1 occupy 2 voxels because floor(-0.01)=-1. Frame "camera" versus expected "base" reports False without modifying the coordinates.
