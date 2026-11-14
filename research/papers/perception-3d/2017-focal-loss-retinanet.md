---
schema_version: 1
paper_id: "2017-focal-loss-retinanet"
title: "Focal Loss for Dense Object Detection"
authors: ["Lin, Tsung-Yi","Goyal, Priya","Girshick, Ross","He, Kaiming","Dollár, Piotr"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1708.02002"
pdf_url: "https://arxiv.org/pdf/1708.02002"
local_pdf: "./2017-focal-loss-retinanet.pdf"
sha256: "2e6f45b97007009f32b82a3c19f35638d8da7022d8d4e4416b9078de91339f71"
bytes: 1297358
pages: 10
topics: ["perception-3d","focal-loss-retinanet"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Dense predictions supply class probabilities, focal weighting changes each example’s contribution, and the detector combines classification with box regression.","nodes":[{"id":"stage-1","title":"Form binary class probabilities","detail":"Use sigmoid probabilities for each dense class target.","column":0,"row":0,"section":"Form binary class probabilities","problem_slugs":[],"planned_problems":["Convert Dense Class Logits to Independent Sigmoid Probabilities"]},{"id":"stage-2","title":"Apply focal weighting","detail":"Downweight confident correct examples while retaining hard-example gradients.","column":1,"row":0,"section":"Apply focal weighting","problem_slugs":[],"planned_problems":["Implement stable sigmoid focal loss","Compare gradient weights across confidence levels"]},{"id":"stage-3","title":"Reduce over valid anchors","detail":"Mask ignored examples and normalize the classification/regression objectives deliberately.","column":2,"row":0,"section":"Reduce over valid anchors","problem_slugs":[],"planned_problems":["Apply valid/ignored anchor masks and reductions"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"class logits"},{"from":"stage-2","to":"stage-3","label":"per-anchor losses"}]}
---

## Core paper explanation

Focal loss reduces the training weight of easy classification examples so dense detectors are not dominated by large numbers of obvious background locations. RetinaNet combines this objective with a feature pyramid and dense prediction heads. The key idea is a differentiable modulation of cross-entropy, not simply deleting all easy negatives.

## Execution flow

Dense predictions supply class probabilities, focal weighting changes each example’s contribution, and the detector combines classification with box regression.

### Form binary class probabilities

For logit $z$ and target $y\in\{0,1\}$, let $p=\sigma(z)$ and

$$
p_t=\begin{cases}p,&y=1,\\1-p,&y=0.\end{cases}
$$

Thus $p_t$ is the probability assigned to the true label. The stable implementation should work from logits rather than evaluating $\log(\sigma(z))$ naively for extreme inputs.




**Planned component problem:** Convert Dense Class Logits to Independent Sigmoid Probabilities. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Apply focal weighting

With class-balancing factor $\alpha_t$ and focusing exponent $\gamma\ge0$,

$$
\operatorname{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t.
$$

At $\gamma=0$, this becomes weighted cross-entropy. For $\gamma=2$, an easy example with $p_t=0.99$ receives modulation $10^{-4}$, while $p_t=0.5$ receives0.25. The modulating factor remains in the computation graph; detaching it changes the gradient.


**Planned component problems:** Implement stable sigmoid focal loss; Compare gradient weights across confidence levels. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Reduce over valid anchors

For validity mask $m_i$ and a declared normalizer $Z$, a batch reduction is

$$
\mathcal L_{\mathrm{cls}}=\frac{\sum_i m_i\operatorname{FL}_i}{Z}.
$$

The detector’s positive-anchor normalization and ignored-label semantics must be preserved. An all-background batch needs an explicit nonzero normalization policy. Focal weighting addresses imbalance in supervision; it does not replace box matching or localization loss.


**Planned component problems:** Apply valid/ignored anchor masks and reductions. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Convert Dense Class Logits to Independent Sigmoid Probabilities.
- Implement stable sigmoid focal loss.
- Compare gradient weights across confidence levels.
- Apply valid/ignored anchor masks and reductions.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A dense detector may see mostly background during routine robot operation. Focal loss can make training focus on difficult examples, but rare sensor faults or mislabeled objects can also become hard examples with high influence. Inspect label quality and per-class performance rather than assuming more focusing is always better.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1708.02002) · [Open-access manuscript](https://arxiv.org/pdf/1708.02002)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
