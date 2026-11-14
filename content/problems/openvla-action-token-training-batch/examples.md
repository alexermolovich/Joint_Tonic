## Example 1

prompts=[[7],[6,7]], actions=[[8],[9]], pad0,eos1,vocab10 gives inputs[[7,8,1,0],[6,7,9,1]], labels[[-100,8,1,-100],[-100,-100,9,1]], lengths[3,4].

## Example 2

prompt[[2]], actions[[3,4]], pad0,eos1,vocab5 gives input[[2,3,4,1]], labels[[-100,3,4,1]], all attention entriesTrue.
