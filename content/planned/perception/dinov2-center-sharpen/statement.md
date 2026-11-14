# Center and Sharpen Teacher Probabilities

Implement center_sharpen(logits, center, temperature). logits and center are finite NumPy float64 arrays shaped (B,K) and (K,), with 1<=B,K<=1024, at most1,000,000 logits, and absolute values<=1e6. temperature is a built-in int/float excluding bool in [1e-4,1e4]. Compute row softmax((logits-center)/temperature) using a stable maximum subtraction. Return new float64 probabilities (B,K), preserving inputs and supporting noncontiguous arrays. Rows sum to1 within rtol1e-7,atol1e-9; underflow to0 is allowed. TypeError for non-array logits/center; ValueError for all other violations. No gradient contract (NumPy), center update, student loss, or Sinkhorn balancing. Coordinates are dimensionless prototype scores, not robot positions; center corresponds to the supplied training snapshot. This is the centering/sharpening variant discussed in the DINO family. DINOv2's improved training uses Sinkhorn-Knopp normalization; this component must not be presented as that full target-balancing procedure.

## Examples

## Centering changes the target

logits=[[2,0],[0,2]], center=[1,0], temperature=1. Output approximately [[0.7310585786,0.2689414214],[0.0474258732,0.9525741268]]. The second row's centered logits are [-1,2].

## Sharpen a fixed margin

logits=[[1,0]], center=[0,0], temperature=.5. Output [[0.8807970780,0.1192029220]]. At temperature1 this would be [0.7310585786,0.2689414214]. Smaller positive temperature concentrates mass on the larger centered score.
