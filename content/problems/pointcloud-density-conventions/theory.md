# Validate Point-Cloud Density and Coordinate Conventions

## Intuition

An array can have three columns while using the wrong units or frame. A useful cloud audit preserves that metadata and separately measures how samples occupy a fixed voxel grid.

## Math and spatial trace

For input point $p_i$ and unit scale $s$ (1 for meters, 0.01 for centimeters, 0.001 for millimeters), let $x_i=s p_i$ in meters. With voxel side $h>0$ meters,
$$v_i=\lfloor x_i/h\rfloor\in\mathbb Z^3,\qquad K=|\{v_i\}|,\qquad \rho=N/K.$$
Define $\rho=0$ for $N=0$. This is points per occupied voxel, not points per cubic meter. Extent on axis $j$ is $e_j=\max_i x_{ij}-\min_i x_{ij}$, with zero extent for empty clouds.

| x (m) | h (m) | voxel index |
|---|---|---|
| -0.01 | 1 | -1 |
| 0 | 1 | 0 |
| 0.5 | 1 | 0 |
| 1 | 1 | 1 |

The three centimeter example points convert to 0,0.5,1 meters: two occupied voxels and density $3/2=1.5$. Truncating toward zero would incorrectly merge a negative boundary point with the origin cell.

## Why this matters on a robot

Cloud density changes with range, occlusion and sensor settings. A density change is evidence, not a complete quality verdict. Frame compatibility comes from explicit labels; a symmetric point cloud cannot reveal whether its axes were swapped. A converter must not silently declare a frame mismatch repaired.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1612.00593). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
