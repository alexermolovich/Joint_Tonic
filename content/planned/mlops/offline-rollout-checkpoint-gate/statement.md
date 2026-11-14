# Select a Checkpoint with Offline and Rollout Gates

Implement select_checkpoint(candidates, max_loss, min_success, min_trials) -> str | None.

candidates is a Python list of0–10,000 tuples (checkpoint_id,validation_loss,successes,trials). IDs are unique ASCII strings [a-z][a-z0-9_-]{0,63}. loss is a built-in non-bool int/float, finite in[0,1e6]. successes and trials are built-in non-bool ints with0<=successes<=trials<=1,000,000. A zero-trial candidate is allowed as missing evidence.

max_loss uses the same scalar loss type/range. min_trials is a built-in non-bool int in[1,1,000,000]. min_success is a tuple(p,q) of built-in non-bool ints satisfying0<=p<=q and1<=q<=1,000,000. It specifies an exact rational minimum success rate p/q, not a floating percentage.

A candidate is eligible iff loss<=max_loss, trials>=min_trials and successes*q>=p*trials. Boundary equality passes. Select the eligible candidate with highest exact success ratio, then lowest loss, then ASCII ID. Return its ID or None if no candidate is eligible, including an empty collection. Never compute a success rate for a zero-trial candidate. Preserve all inputs.

All malformed containers, records, IDs, duplicates, ranges or thresholds raise ValueError even for an empty candidate list. This is a deterministic supplied-evidence decision; it does not run a policy, establish statistical confidence, deploy a model or alter files.

## Worked examples

### A high-success candidate can fail the offline gate

~~~python
select_checkpoint([("fit",0.2,8,10),("risky",0.8,9,10),("short",0.1,1,1)],
                  max_loss=0.3,min_success=(4,5),min_trials=10)
# "fit"
~~~

fit passes at exactly80% success. risky exceeds maximum loss; short lacks rollout coverage.

### An exact success boundary with deterministic ties

~~~python
select_checkpoint([("zeta",0.1,1,2),("alpha",0.1,5,10)],
                  max_loss=0.1,min_success=(1,2),min_trials=2)
# "alpha"
~~~

Both ratios equal1/2 and both losses meet the gate exactly. Equal ratios and losses use the ID tiebreak. With min_trials=11 the result is None.

## Source and scope

robomimic motivates comparing offline objectives with rollout behavior. These explicit thresholds and deterministic selection rules are an original teaching policy, not a claim about the paper's exact checkpoint selection implementation. [Primary source](https://arxiv.org/abs/2108.03298).

