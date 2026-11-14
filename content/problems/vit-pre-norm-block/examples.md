# Worked examples

1. With q,k,v,o,w1,w2 and both biases all zero, gamma all ones and beta zeros, output equals tokens exactly: both residual branches contribute zero.
2. For one token `[2,4]`, zero attention branch and zero w1,w2, b2=`[1,-1]`, output is `[3,3]`. No final layer normalization is applied.
