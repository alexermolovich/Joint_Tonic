# Infer a Schema from Robot Episodes

## Intuition

Before enforcing a robot dataset contract, inspect what was actually recorded. Shapes and ranges can be summarized mechanically; meanings such as radians versus degrees must come from metadata. The output is a proposal for a human or a later validation policy.

## Reduce samples, preserve channels

Let E be the number of episodes. For signal f, let $\mathcal I_f$ be the episodes containing it, and let $X^{(i,f)}\in\mathbb R^{T_{if}\times D_f}$ be its recorded values. The unit and frame must agree across those occurrences. For channel j,

$$
m_{f,j}=\min_{i\in\mathcal I_f,\ 0\le t<T_{if}}X^{(i,f)}_{t,j},
\qquad
M_{f,j}=\max_{i\in\mathcal I_f,\ 0\le t<T_{if}}X^{(i,f)}_{t,j}.
$$

Both extrema retain that channel's physical units. All occurrences are nonempty, so an observed signal always has defined extrema. A proposed presence requirement is

$$
r_f=\mathbf1[|\mathcal I_f|=E].
$$

An empty episode contributes to E but contributes no invented zeros. Missing data must not become a plausible physical reading.

## Visual: channel ranges across episodes

| Signal/channel | Episode0 observations | Episode1 observations | Min, max |
|---|---|---|---|
| joints/0 | 0,1 | -1 | -1,1 |
| joints/1 | 2,4 | 3 | 2,4 |
| force/0 | 5 | absent | 5,5 |

This table is the static reduction diagram and text alternative. Each channel is reduced independently; flattening all joint coordinates would return the wrong two-dimensional contract.

A streaming reducer stores current minima/maxima and occurrence counts. It need not concatenate all episode arrays, which avoids unnecessary memory use. Reject a width or metadata conflict before combining values from incompatible signals.

## Why this matters on a robot

A merged dataset might label a joint signal in radians in one collection and degrees in another. Numerical extrema alone cannot reveal the correct conversion, so this contract rejects the mismatch. Ranges inferred from successful demonstrations also omit failures and unusual states; using those extrema as hard motor limits would be unjustified.

## Check your understanding

1. Does an absent force signal contribute a zero?
2. Does required=True prove the sensor will always be available?

## Sources and prerequisites

The paper motivates proposing schemas from observed data and reviewing them before enforcement. This numeric robot-signal schema and range policy are original; observed extrema are not hardware limits or a guarantee about unseen data. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/), Sections3–4: schema-based validation and schema inference. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
