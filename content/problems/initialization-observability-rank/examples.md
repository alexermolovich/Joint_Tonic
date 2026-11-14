# Worked examples

1. J=`[[2.,0.],[0.,1.]]`, scales and standard deviations all 1, cutoff 0.001: singular values `[2.,1.]`, rank 2, condition 2 and zero unobservable projector.
2. J=`[[1.,0.]]` with unit scales/std gives rank 1, singular values `[1.,0.]`, condition +Inf and projector `[[0.,0.],[0.,1.]]`. The second scaled parameter direction has no measurement support.
