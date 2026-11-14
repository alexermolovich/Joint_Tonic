# Worked examples

## A rank-one update changes the forward value

For x=[[[1,2]]], base_weight=[[1,0],[0,1]], adapter_down=[[1,-1]], adapter_up=[[2],[3]], alpha=2, use one common floating tensor dtype. The low-rank hidden value is -1. The scaled update is [-4,-6], so return [[[-3,-4]]]. For the sum of outputs, the x gradient is [[[11,-9]]]; base_weight receives no gradient.

## A zero up-projection preserves the base prediction

For x=[[[3,4]]], base_weight=[[2,0],[0,-1]], adapter_down=[[1,1]], adapter_up=[[0],[0]], alpha=1, return [[[6,-4]]]. The adapter_down gradient is zero at this point, but each adapter_up entry has gradient 7 for the sum of outputs. A zero initial adapter update does not mean all adapter learning is disabled.
