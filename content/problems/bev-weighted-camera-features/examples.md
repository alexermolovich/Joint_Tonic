# Worked examples

## Ignore an invalid camera sample

B=Q=1,C=2,S=1,D=2; features=[[[[[2,4]],[[10,20]]]]], weights=[[[[1],[3]]]], valid=[[[[True],[False]]]]. Return output=[[[2,4]]], observed=[[True]]. Invalid weight3 contributes neither numerator nor denominator.

## Fuse two available views

Use the same features/weights but both valid. Return output=[[[8,16]]], observed=[[True]]. (1*[2,4]+3*[10,20])/4=[8,16]. With both weights zero return [[[0,0]]] and [[False]].
