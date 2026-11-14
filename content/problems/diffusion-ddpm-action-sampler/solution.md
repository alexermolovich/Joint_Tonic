## Approach

Validate scheduler/tensor shapes, calculate forward cumulative products, then apply the stated posterior mean and variance from the last index to zero. Stack independent state snapshots.

O(K*H*D) time and trace storage.
