## Example 1

image=[[1,2]], state=[[3,4]], text=[[5,6]], layout=[[2,0],[0,0],[1,0]] returns tokens=[[5,6],[1,2],[3,4]], modalities=[2,0,1].

## Example 2

image=[[7]], state=empty((0,1)), text=empty((0,1)), layout=[[0,0],[0,0]] returns [[7],[7]] and [0,0]. Repetition is intentional, not deduplicated.
