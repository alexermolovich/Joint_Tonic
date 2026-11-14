## Example 1

modalities=[0,1,2], present=[[True,False,True]] returns [[[True,False,False],[False,False,False],[True,False,True]]].

## Example 2

modalities=[2], present=[[False],[True]] returns [[[False]],[[True]]]. Presence varies by batch, even for one shared modality sequence.
