# Worked examples

### A lower offline loss can lose in rollouts

~~~python
compare_checkpoint_metrics([("early",0.1,1,10),("later",0.2,8,10)])
# {"offline_order":["early","later"],
#  "rollout_order":["later","early"],"disagree":True}
~~~

The lower loss does not imply that the policy recovers from states reached by its own actions.

### Equal ratios retain a deterministic order

~~~python
compare_checkpoint_metrics([("zeta",0.3,1,2),("alpha",0.3,5,10)])
# {"offline_order":["alpha","zeta"],
#  "rollout_order":["alpha","zeta"],"disagree":False}
~~~

1/2 and5/10 are exactly equal; ASCII checkpoint ID breaks both ties.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

