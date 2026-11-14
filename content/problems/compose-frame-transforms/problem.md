# Compose and Invert Coordinate Transforms

Implement **compose_transforms(first, second)**. Each input is a dict with required keys matrix, target, source, stamp and unit; ignore extra keys.

matrix is a finite real integer/floating array-like (4,4), with translation magnitude per component <=1e6. Reject bool, complex, string or object matrix dtypes. Its last row is [0,0,0,1] within atol=1e-9, rtol=0. Its rotation R satisfies R.T@R=I and det(R)=1 with the same absolute tolerance. Do not repair invalid matrices.

target and source are nonempty strings without surrounding whitespace. first.source must equal second.target. Both unit fields must equal the string "m". Each stamp is a finite real Python or NumPy scalar (not bool) in [-1e6,1e6]; stamps must be exactly equal. Validate frame/unit/time compatibility before matrix multiplication.

first means a-from-b; second means b-from-c. Return a tuple of independent float64 arrays (T_ac,T_ca), each (4,4). Compute rotation R_ac=R_ab@R_bc and translation t_ac=R_ab@t_bc+t_ab; use an exact [0,0,0,1] bottom row. Invert rigidly with rotation R_ac.T and translation -R_ac.T@t_ac. Preserve inputs and return new storage.

Every documented violation raises ValueError. Same target/source labels are permitted (including a chain that returns to its starting frame). No calibration estimation or interpolation across timestamps.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.

## Worked examples

### A mount offset rotates with the base

first: target="world", source="base", stamp=2, unit="m", matrix=[[0,-1,0,1],[1,0,0,0],[0,0,1,0],[0,0,0,1]].

second: target="base", source="camera", stamp=2, unit="m", matrix=[[1,0,0,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]].

Return T_ac=[[0,-1,0,1],[1,0,0,1],[0,0,1,0],[0,0,0,1]] and T_ca=[[0,1,0,-1],[-1,0,0,1],[0,0,1,0],[0,0,0,1]].

### Two translations

Use the same labels/unit/time. First rotation is identity with translation [2,0,0]; second is identity with translation [0,3,0].

T_ac has identity rotation and translation [2,3,0]; T_ca has identity rotation and translation [-2,-3,0]. Camera point [1,1,0] becomes world point [3,4,0] and returns unchanged.

## Hints

1. Check the middle frame labels, units and timestamps before multiplying matrices.

2. Rotate the second translation by the first rotation.

3. The inverse translation is -R.T@t, not merely -t.
