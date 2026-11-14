# Concatenate Local and Global Features for Segmentation

Implement concat_local_global(local, global_features). Inputs are finite NumPy arrays of same dtype float32 or float64. local shape (B,N,D), global_features shape (B,G); 0<=B,N<=1024, 1<=D,G<=4096; every input and output at most1,000,000 elements. For each cloud b and point n return local[b,n,:] followed by global_features[b,:]. Preserve dtype, order, values and inputs; return independent storage. B=0 or N=0 returns correctly shaped empty output. Noncontiguous inputs supported. TypeError for non-array inputs; ValueError for all other violations including shape/dtype/limits/nonfinite data. Features are dimensionless learned coordinates, not XYZ; each cloud's local/global features describe the same upstream frame and observation. No pooling, MLP, masks, segmentation classifier, or coordinate registration is performed.

## Examples

## One cloud, two points

local=[[[1,2],[3,4]]], global_features=[[10,20,30]], float64. Output [[[1,2,10,20,30],[3,4,10,20,30]]]. The same cloud context is repeated, not interleaved.

## Keep clouds independent

local=[[[1]],[[2]]], global_features=[[10,11],[20,21]], float32. Output [[[1,10,11]],[[2,20,21]]]. Cloud0 never receives cloud1's context.
