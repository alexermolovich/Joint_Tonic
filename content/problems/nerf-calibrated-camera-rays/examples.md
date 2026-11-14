# Worked examples

1. With identity intrinsics/pose, pixels `[[0,0],[1,0]]` yield origins `[[0,0,0],[0,0,0]]`, directions `[[0,0,1],[1/√2,0,1/√2]]`.
2. With fx=fy=2,cx=cy=1, pixel `[[1,1]]` and identity rotation plus translation `[3,0,2]`, the ray starts `[3,0,2]` and points `[0,0,1]`. Translation changes origin, never direction.
