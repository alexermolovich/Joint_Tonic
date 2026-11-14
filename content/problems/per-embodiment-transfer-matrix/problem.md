# Build a Per-Embodiment Transfer Matrix

Implement build_transfer_matrix(sources, targets, records) -> dict.

sources and targets are Python lists of1–128 unique ASCII IDs matching [a-z][a-z0-9_-]{0,63}. Their provided order defines matrix axes: row=source training-policy condition, column=target evaluated embodiment. The labels are caller-defined experiment identities, not inferred robot similarity.

records is a Python list of0–100,000 tuples(source,target,successes,trials). Both IDs must occur on their declared axis. successes/trials are built-in non-bool ints with1<=trials<=1,000,000 and0<=successes<=trials. Repeated pairs, including identical records, contribute additional trial evidence and are summed.

Return exactly four new arrays of shape(len(sources),len(targets)):
- successes: int64 summed successes per cell, zero when absent.
- trials: int64 summed trials per cell, zero when absent.
- observed: bool, true iff cell trial count>0.
- rates: float64 successes/trials for observed cells, NaN for absent cells.

Each array has independent storage from inputs and from the other outputs. Preserve input lists/records. Rates use rtol=1e-12,atol=1e-12 with NaN only at unobserved cells; integer/boolean values and axis order are exact. Empty records produce zero counters, false observed and all-NaN rates. All malformed types, lengths, duplicate axis IDs, unknown record IDs, nonpositive trials or invalid counts raise ValueError.

This matrix reports observations. It does not subtract a baseline, estimate transfer significance, assume missing cells failed or execute a policy. Comparisons require matching task protocols and separate uncertainty analysis.

## Worked examples

### Pool counts, not percentages

~~~python
build_transfer_matrix(["solo","mixed"],["arm_a","arm_b"],
 [("mixed","arm_b",1,2),("mixed","arm_b",9,10),("solo","arm_a",2,4)])
# successes = [[2,0],[0,10]]
# trials    = [[4,0],[0,12]]
# observed  = [[True,False],[False,True]]
# rates     = [[0.5,NaN],[NaN,10/12]]
~~~

The mixed-to-arm_b rate is10/12, not the average of0.5 and0.9.

### Preserve axis order and measured failure

~~~python
build_transfer_matrix(["mixed"],["arm_b","arm_a"],[("mixed","arm_a",0,3)])
# successes = [[0,0]]
# trials    = [[0,3]]
# observed  = [[False,True]]
# rates     = [[NaN,0.0]]
~~~

The first target is unmeasured; the second has three measured failures.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864).

