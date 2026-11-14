## Example 1

sequences=[[[1],[2]],[[3]]], modalities=[[0,2],[1]] returns tokens=[[[1],[2]],[[3],[0]]], modalities=[[0,2],[1,-1]], present=[[True,True],[True,False]], lengths=[2,1].

## Example 2

sequences=[empty((0,2)),[[0,0]]], modalities=[empty integer vector,[2]] returns tokens=zeros((2,1,2)), modalities=[[-1],[2]], present=[[False],[True]], lengths=[0,1]. The real zero token is present.
