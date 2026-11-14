# Worked examples

## A non-monotone vocabulary

bins=[[0,2],[1,0]], vocabulary=[41,7,99], termination=[0,1], all int64.

Return [[0,41,99],[1,7,41]]. Bin1 means token7 even though the vocabulary is not numerically sorted.

## A single action channel

bins=[[1]], vocabulary=[100,3], termination=[0]. Return [[0,3]]. For bins shaped(0,1) and termination shaped(0,), return an empty array shaped(0,2).
