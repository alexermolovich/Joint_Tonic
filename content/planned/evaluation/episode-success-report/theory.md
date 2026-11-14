# Report Robot Policy Success Without Hiding Missing Tasks: theory

## Intuition

A policy can look strong when the evaluation repeats its easiest task many times. A useful report preserves both the experience-weighted outcome and the performance across the intended task set. It also distinguishes reaching the goal from doing so without collisions or human intervention.

## Episodes and denominators

For task $k$, let $n_k$ be its observed episode count and $s_k$ its successful outcomes. A task with evidence has success rate

$$
a_k=\frac{s_k}{n_k}.
$$

Timeout, intervention, and collision rates use the same task count but different indicators. A collision flag is independent of the outcome: a robot may reach the goal after contacting something. Recording both facts allows a later release policy to reject unsafe behavior without corrupting the raw evidence.

The pooled, or micro, success rate weights every episode equally:

$$
a_{\mathrm{micro}}=\frac{\sum_k s_k}{\sum_k n_k}.
$$

If all K expected tasks have evidence, the macro rate weights each task equally:

$$
a_{\mathrm{macro}}=\frac1K\sum_k a_k,\qquad
\mathrm{coverage}=\frac{|\{k:n_k>0\}|}{K}.
$$

All rates are dimensionless. A missing denominator is not zero performance and is not perfect performance. This contract represents unobserved task rates as None and withholds macro success until the planned task set is covered.

## Worked policy example

Task A has one success and one timeout, so its success rate is 0.5. Task B has one success, so its rate is 1.0. Micro success is $2/3$ because two of three episodes succeeded. Macro success is $(0.5+1)/2=0.75$. Neither value is universally better; they answer different weighting questions.

If Task B was never attempted, coverage is 0.5 and macro success is unavailable. Reporting only Task A as the entire benchmark would hide the evaluation gap.

## Visual explanation

Show task rows with episode counts, success bars, collision markers, and explicit missing-evidence cells. Place micro and macro summaries beside their formulas and denominators. A text table exposes the same quantities and the ordered list of missing tasks.

## Robot relevance and failure modes

Repeatedly rerunning failed episodes until they pass changes the sampling protocol. Pooling tasks can hide a weak manipulation skill; dropping interventions can inflate success. This lesson makes those accounting choices visible before learners compare robot-policy papers. Confidence intervals, scenario diversity, reset policies, and hardware versions remain necessary extensions for credible real-world evaluation.

