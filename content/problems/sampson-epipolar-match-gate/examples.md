# Worked examples

1. F=`[[0.,0.,0.],[0.,0.,-1.],[0.,1.,0.]]`, source `[[0.,0.]]`, target `[[3.,2.]]`: squared Sampson error is 2 square pixels. Threshold sqrt(2) accepts the pair; threshold 1 rejects it.
2. Change the target to `[[3.,0.]]`: the epipolar residual and squared error are zero, so threshold 0 accepts. With valid=False, squared_error is +Inf and the pair is rejected despite zero residual.
