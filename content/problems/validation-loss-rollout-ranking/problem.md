# Compare Validation Loss with Rollout Success

Implement compare_checkpoint_metrics(records: list[tuple[str,float,int,int]]) -> dict.

Each record is (checkpoint_id, validation_loss, successes, trials). records is a Python list of1–10,000 tuples. IDs are unique strings matching ASCII [a-z][a-z0-9_-]{0,63}. validation_loss is a built-in non-bool int/float, finite and0<=loss<=1e6. successes/trials are built-in non-bool ints with1<=trials<=1,000,000 and0<=successes<=trials.

Return exactly:
- offline_order: all checkpoint IDs sorted by ascending loss, then ASCII ID.
- rollout_order: all IDs sorted by descending exact ratio successes/trials, then ASCII ID.
- disagree: Python bool, true iff the first ID in the two lists differs.

Compare ratios exactly as rational numbers, not rounded displayed percentages. The records are assumed to use the same task protocol and validation-loss definition; no confidence weighting, correlation coefficient, significance claim or real policy execution occurs. Both orders contain every ID once, and output lists are independent of inputs and each other. Preserve all inputs. Every malformed record, bound, duplicate ID or empty outer list raises ValueError.

## Worked examples

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

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298).

