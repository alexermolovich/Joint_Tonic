# Report Performance by Demonstration Quality

Implement quality_performance(records: list[tuple[str,str,bool]]) -> dict.

Each record is (quality_id,task_id,success). records is a Python list of0–100,000 tuples. Quality/task labels match ASCII [a-z][a-z0-9_-]{0,63}; success is a built-in bool. Labels describe the training-demonstration condition and evaluated task supplied by the experiment, not inferred skill judgments. Identical tuples count as separate rollout trials. At most10,000 distinct (quality,task) pairs are allowed.

Return exactly:
- by_slice: list of (quality,task,trials,successes,rate), sorted by(quality,task).
- by_quality: list of (quality,trials,successes,pooled_rate,macro_task_rate), sorted by quality.

For each slice rate=successes/trials. A quality's pooled_rate sums successes and trials across its observed tasks, then divides. macro_task_rate averages its observed task rates with equal task weight; do not invent absent tasks or zeros. All rates are Python floats; counts are built-in ints, rows are tuples. Compute float64 semantics with rtol=1e-12,atol=1e-12; counts/order/structure are exact. Empty input returns both lists empty. Preserve inputs.

Every malformed container, tuple, label, success type or exceeded bound raises ValueError. No confidence intervals, comparison across unmatched task coverage, policy execution or causal conclusion about demonstration quality is included.

## Worked examples

### A frequent easy task hides a failed hard task

~~~python
records = [("expert","easy",True)]*9 + [("expert","hard",False)]
quality_performance(records)
# {"by_slice":[("expert","easy",9,9,1.0),("expert","hard",1,0,0.0)],
#  "by_quality":[("expert",10,9,0.9,0.5)]}
~~~

Pooled success is9/10. Equal weighting of the two task rates gives(1+0)/2=0.5.

### Separate quality conditions

~~~python
quality_performance([("mixed","lift",False),("expert","lift",True),
                     ("mixed","lift",True)])
# {"by_slice":[("expert","lift",1,1,1.0),("mixed","lift",2,1,0.5)],
#  "by_quality":[("expert",1,1,1.0,1.0),("mixed",2,1,0.5,0.5)]}
~~~

Quality labels define separate experiment groups even when task labels match.

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298).

