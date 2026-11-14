# Worked examples

## A mount offset rotates with the base

first: target="world", source="base", stamp=2, unit="m", matrix=[[0,-1,0,1],[1,0,0,0],[0,0,1,0],[0,0,0,1]].

second: target="base", source="camera", stamp=2, unit="m", matrix=[[1,0,0,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]].

Return T_ac=[[0,-1,0,1],[1,0,0,1],[0,0,1,0],[0,0,0,1]] and T_ca=[[0,1,0,-1],[-1,0,0,1],[0,0,1,0],[0,0,0,1]].

## Two translations

Use the same labels/unit/time. First rotation is identity with translation [2,0,0]; second is identity with translation [0,3,0].

T_ac has identity rotation and translation [2,3,0]; T_ca has identity rotation and translation [-2,-3,0]. Camera point [1,1,0] becomes world point [3,4,0] and returns unchanged.
