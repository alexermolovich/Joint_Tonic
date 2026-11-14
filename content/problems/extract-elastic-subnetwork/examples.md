# Worked examples

### Center crop
For `weights=[np.arange(9,dtype=np.float64).reshape(1,1,3,3)]`, depth1,width1,kernel1 returns `[np.array([[[[4.]]]])]`.

### Depth and width both shrink
For two layers filled with2 and3 respectively, each shape(2,2,3,3), depth1,width1,kernel3 returns one independent array of shape(1,1,3,3) filled with2.
