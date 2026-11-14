## Worked examples

**Example 1.** Actions `[[[0]]]`, all-zero kernel and conditioning/time weights, head `[[1]]`, bias `[2]`: output predicted noise is `[[[2]]]`.

**Example 2.** Use action value `1`, center kernel value `1`, other kernel entries zero, head `1`, bias `0` and zero conditioning/time weights. Output is `[[[1/(1+exp(-1))]]]`, approximately `[[[0.73105858]]]`; do not add the original action.
