## Example 1

Rewards[0,exp(1)-1], bins[-1,0,2] -> symlog[0,1], targets[[0,1,0],[0,.5,.5]], reconstructed equals supplied rewards.

## Example 2

Rewards[-100,100],bins[-1,0,1] -> endpoint one-hot rows[1,0,0],[0,0,1], reconstructed[-(exp(1)-1),exp(1)-1].
