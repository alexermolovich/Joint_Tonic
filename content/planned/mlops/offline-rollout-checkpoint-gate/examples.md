# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

