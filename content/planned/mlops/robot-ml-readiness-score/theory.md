# Score a Robot ML System for Production Readiness

## Intuition

A robot team may automate model accuracy checks while manually checking calibration and never testing rollback. An overall average can make that system look better as more accuracy tests are added. A minimum across categories keeps the weakest area visible.

## Credits and category sums

Let c index one of the four fixed categories, and let $s_{c,j}$ be the supplied status of check j in category c. Define credit w in dimensionless points:

$$
w(s)=
\begin{cases}
0,&s=\mathrm{none},\\
1/2,&s=\mathrm{manual},\\
1,&s=\mathrm{automated}.
\end{cases}
\qquad
S_c=\sum_j w(s_{c,j}),\qquad S=\min_c S_c.
$$

An empty sum is zero. Each category has at most seven checks, so $0\le S\le7$. Credits are exact halves and integers, so these bounded sums have exact binary floating representations. There is no numerical tolerance issue.

Automation describes how evidence is produced. A perfectly automated failing test still earns automation credit in this narrow questionnaire. A separate release gate examines pass/fail outcomes; readiness practice and permission to release answer different questions.

## Visual: coverage ledger

| Category | Evidence credits | Sum |
|---|---|---:|
| data | 1 + 0.5 | 1.5 |
| model | 1 | 1 |
| infrastructure | 0.5 + 0 | 0.5 |
| monitoring | 1 + 1 | 2 |

Read down to compare the four sums. The final minimum is0.5. This ledger is also the static text alternative. Raising monitoring from2 to3 leaves the minimum unchanged; improving infrastructure can change it.

## Why this matters on a robot

Metrics cannot compensate for missing calibration checks or an untested recovery process. The score helps organize engineering effort but is sensitive to which checks a team supplied. Splitting one check into many can inflate sums, and automation can repeatedly test the wrong invariant. The upstream checklist needs review.

## Check your understanding

1. Does a score of7 certify that the candidate model passed its tests?
2. Why not average the four categories?

## Sources and prerequisites

The half-point/manual, full-point/automated and minimum-category aggregation follows the paper. Supplied check lists and robot examples are original; this function does not reproduce the paper's full28-check questionnaire or certify operational safety. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/), SectionVI.A: Computing an ML Test Score. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
