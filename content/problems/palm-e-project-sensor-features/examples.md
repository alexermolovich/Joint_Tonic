# Worked examples

## Two sensor tokens and a bias

features=[[[1,2],[3,4]]], weight=[[1,0,-1],[0,2,1]], bias=[0.5,-1,2], valid=[[True,True]].

Return [[[1.5,3,3],[3.5,7,3]]]. The first matrix product is [1,4,1]; adding the bias gives [1.5,3,3].

## A missing token must not receive bias

features=[[[2],[-5]]], weight=[[3,4]], bias=[1,-1], valid=[[True,False]].

Return [[[7,7],[0,0]]]. Multiplying a masked feature by zero before adding bias would incorrectly produce [1,-1] in the invalid row.
