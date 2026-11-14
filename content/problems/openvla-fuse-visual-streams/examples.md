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
