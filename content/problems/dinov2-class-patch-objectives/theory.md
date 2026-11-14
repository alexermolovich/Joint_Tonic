# Combine Class-Token and Masked-Patch Objectives

## Intuition

A class token should agree across different crops of one image. A masked patch should agree with the teacher's target at that particular location. Keep those reductions separate: adding more local crops or selecting more masked patches should not automatically scale either mean.

## Stable cross-entropy with fixed targets

Let $\ell_{bvk}$ be student class logits for image $b$, view $v$, and prototype $k$. There are $B$ images, $V$ student views, and $K$ prototypes. The teacher has two global views with target probabilities $q_{btk}$. At positive student temperature $\tau$,

$$
\log p_{bvk}=\ell_{bvk}/\tau-
\log\sum_{j=0}^{K-1}\exp(\ell_{bvj}/\tau).
$$

Use a stable log-softmax operation rather than computing probabilities and then taking their logarithm. Targets are detached probabilities whose rows sum to one. The cross-view class loss is

$$
L_{\mathrm{class}}=
-\frac{1}{2B(V-1)}
\sum_{b=0}^{B-1}\sum_{t=0}^{1}
\sum_{\substack{v=0\\v\ne t}}^{V-1}
\sum_{k=0}^{K-1}q_{btk}\log p_{bvk}.
$$

View labels 0 and 1 identify corresponding global views; omitting v=t removes same-view supervision. Every local student view still receives both global teacher targets.

## Visual: legal view pairs when V=3

| Teacher view | Student 0 | Student 1 | Student 2 (local) |
|---|---|---|---|
| 0 | exclude | include | include |
| 1 | include | exclude | include |

The table is the original static mask diagram and text alternative. There are four included pairs per image. Equal zero logits over two prototypes give log(2) cross-entropy for each normalized teacher row, so the average remains log(2).

## The masked patch branch

Let $z_{bpk}$ be student patch logits, $r_{bpk}$ detached teacher probabilities, and $m_{bp}$ the Boolean selection mask for $P$ aligned patch positions. With $M=\sum_{b,p}m_{bp}$,

$$
L_{\mathrm{patch}}=
\begin{cases}
-\dfrac1M\sum_{b,p}m_{bp}\sum_k r_{bpk}
\log\operatorname{softmax}(z_{bp}/\tau)_k,&M>0,\\
0,&M=0.
\end{cases}
$$

The zero branch must remain connected to the student graph: zero times the sum of student patch logits has the correct value and zero derivative, even when P=0. The final dimensionless loss is

$$
L=\lambda_cL_{\mathrm{class}}+\lambda_pL_{\mathrm{patch}},
$$

with supplied nonnegative weights $\lambda_c,\lambda_p$. This explicit global selected-token mean is a teaching reduction, not a claim to reproduce every distributed weighting detail of DINOv2.

In example 1 the selected patch's logits [log(3),0] yield target probability 3/4. Its loss is log(4/3), while the class mean is log(2). Weighting the patch branch by 2 gives approximately 1.2685113.

## Why this matters on a robot

Global visual similarity can ignore a small contact surface that matters to manipulation. Patch supervision preserves a separate spatial objective, but only if student and teacher positions correspond. A crop-coordinate mismatch supplies precise-looking targets for the wrong location. Accidentally backpropagating through teacher targets also changes the optimization problem.

## Sources and prerequisites

[DINOv2](https://arxiv.org/abs/2304.07193) combines image- and patch-level self-supervision; the [official training implementation](https://github.com/facebookresearch/dinov2/blob/main/dinov2/train/ssl_meta_arch.py) includes additional weighting and regularization. This original bounded exercise supplies normalized targets and omits those additional stages. Prerequisite: [teacher probabilities](/problems/dinov2-center-sharpen), whose centering variant is separate from Sinkhorn balancing.

