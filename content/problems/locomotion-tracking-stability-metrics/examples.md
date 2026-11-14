## Example 1

B=T=1, measured v[.8,.1,.2], w[.1,.2,.3], command[1,0,.5], gravity[0,0,-1], validTrue, scales .25,.25 -> terms [exp(-.2),exp(-.16),.04,.05,0], count1 and same means.

## Example 2

v=w=command0, gravity[1,0,0], validTrue -> [1,1,0,0,1]. ValidFalse gives all-zero terms,count0,all-NaN means. A perfectly upside-down gravity[0,0,1] also has zero tilt penalty; explicitly this surrogate alone cannot certify upright stability.
