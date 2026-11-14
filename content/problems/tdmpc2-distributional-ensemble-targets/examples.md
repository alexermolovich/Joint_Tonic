## Example 1

reward 1,next_values [2,10,4],indices [0,2],not terminated,gamma .5 ->bootstrap 2,td_target 2. With bins[0,log(2),log(3)],reward target [0,1,0],value target [0,0,1].

## Example 2

Same row terminated True ->td_target 1 and value target equals reward target, while reported bootstrap remains 2.
