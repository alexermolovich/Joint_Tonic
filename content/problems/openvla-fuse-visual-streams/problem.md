# Fuse Two Visual Feature Streams Safely

Implement fuse_visual_features(first, second, projection, bias, first_valid, second_valid), returning (fused, valid).

The four floating inputs are finite CPU torch.float32 or torch.float64 tensors with one common dtype and absolute entries <= 100. first is (B,N,C1), second is (B,N,C2), projection is (C1+C2,E), and bias is (E,). Require 1 <= B <= 32, 1 <= N <= 512, 1 <= C1,C2 <= 256 and 1 <= E <= 512. Each input tensor and the fused output contain at most 1,000,000 entries. first_valid and second_valid are CPU torch.bool tensors (B,N). Noncontiguous inputs are supported.

The caller guarantees that the two token rows at each (b,n) correspond to the same image patch, with identical spatial ordering and synchronized observation context. This function cannot infer correspondence from equal shapes. Features and projected coordinates are dimensionless; no metric frame transformation or timestamp alignment occurs.

Set valid = first_valid & second_valid. Concatenate first then second along feature width, apply the supplied affine projection, and set every invalid output row to exact zeros after adding bias. Thus fused = where(valid[...,None], concat(first,second,-1) @ projection + bias, 0). Return fused(B,N,E) with the input floating dtype/device and valid(B,N) as bool. All-false validity is permitted; validate every floating entry even in masked-out rows.

Preserve input values and return independent storage. Gradients must reach both feature tensors, projection and bias wherever they require gradients; invalid rows contribute zero gradients. Do not detach floating inputs. Non-tensor inputs raise TypeError; all dtype/device/shape/bound violations raise ValueError.

This is an original affine fusion exercise motivated by OpenVLA's feature concatenation and projection. It does not implement the trained visual encoders, nonlinear full projector, image preprocessing, token resampling, missing-camera imputation or the language model. The intersection-mask rule is a declared teaching policy.

## Worked examples

## Concatenate channels, then mask after bias

~~~python
first = torch.tensor([[[1.,2.],[8.,9.]]], dtype=torch.float64)
second = torch.tensor([[[3.],[4.]]], dtype=torch.float64)
projection = torch.tensor([[1.,0.],[0.,1.],[2.,-1.]], dtype=torch.float64)
bias = torch.tensor([0.5,1.], dtype=torch.float64)
first_valid = torch.tensor([[True,True]])
second_valid = torch.tensor([[True,False]])
~~~

Return fused=[[[7.5,0.],[0.,0.]]] and valid=[[True,False]]. The first joined row [1,2,3] projects to [7,-1], then receives bias. The unavailable second stream invalidates the entire second fused row.

## Different streams have different projection columns

For first=[[[2.]]], second=[[[5.]]], projection=[[1.],[10.]], bias=[0.], and both masks true, return fused=[[[52.]]] and valid=[[True]]. Swapping the concatenation order would produce 25 instead. If either mask is false, that output row is zero.


# Worked examples

## Concatenate channels, then mask after bias

~~~python
first = torch.tensor([[[1.,2.],[8.,9.]]], dtype=torch.float64)
second = torch.tensor([[[3.],[4.]]], dtype=torch.float64)
projection = torch.tensor([[1.,0.],[0.,1.],[2.,-1.]], dtype=torch.float64)
bias = torch.tensor([0.5,1.], dtype=torch.float64)
first_valid = torch.tensor([[True,True]])
second_valid = torch.tensor([[True,False]])
~~~

Return fused=[[[7.5,0.],[0.,0.]]] and valid=[[True,False]]. The first joined row [1,2,3] projects to [7,-1], then receives bias. The unavailable second stream invalidates the entire second fused row.

## Different streams have different projection columns

For first=[[[2.]]], second=[[[5.]]], projection=[[1.],[10.]], bias=[0.], and both masks true, return fused=[[[52.]]] and valid=[[True]]. Swapping the concatenation order would produce 25 instead. If either mask is false, that output row is zero.
