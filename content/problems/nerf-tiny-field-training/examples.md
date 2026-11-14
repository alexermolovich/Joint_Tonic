

Use one ray, sample and feature, feature value 1, interval 1 meter, zero initial weight/bias, and black target/background. Density is $\log2$, opacity $1/2$, color $1/2$ in every channel and rendered RGB $1/4$. The mean RGB loss is $1/16$. The raw density gradient is $1/16$ and each raw color gradient is $1/48$. Weight and bias have the same gradient, so $n=\sqrt{1/96}<1$.

With learning rate $0.1$, the new weight row and bias both equal $[-1/160,-1/480,-1/480,-1/480]$. The next density logit is $-1/80$ and each color logit is $-1/240$. This concrete trace checks background-aware rendering, batch normalization and simultaneous updates.

For a zero-error example, use the same initial field but set target and background to $[.5,.5,.5]$. The rendered RGB is exactly that same value; all gradients remain zero and any allowed number of updates leaves parameters unchanged.

