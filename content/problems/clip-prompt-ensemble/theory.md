# Build a class direction from several descriptions

## Intuition

A single wording can bias a zero-shot classifier. Prompt ensembling represents each class with several descriptions, then combines their directions. Normalization before averaging prevents a prompt's feature magnitude from giving it extra influence.

## Three normalizations

Let image features be $V\in\mathbb R^{B\times D}$ and text features $T\in\mathbb R^{C\times P\times D}$. C is the number of classes and P the prompts per class. All coordinates are dimensionless. Define

$$
\bar t_{cp}=\frac{t_{cp}}{\|t_{cp}\|_2},\qquad
m_c=\frac1P\sum_p\bar t_{cp},\qquad
w_c=\frac{m_c}{\|m_c\|_2}.
$$

Normalize each image $\bar v_b=v_b/\|v_b\|_2$, then compare it with the class prototypes:

$$
L_{bc}=\frac{\bar v_b^\top w_c}{\tau},
$$

where positive temperature $\tau$ sets score scale. The returned logits need not sum to one.

## Visual: equal prompt influence

| Prompt vector | Unit direction | Contribution to class mean |
|---|---|---|
| [2,0] | [1,0] | [0.5,0] |
| [0,20] | [0,1] | [0,0.5] |
| Mean | [0.5,0.5] | Norm√0.5 |
| Unit prototype | [√0.5,√0.5] | Final class direction |

This static vector trace is the text alternative. The tenfold raw magnitude difference disappears before ensembling.

## Cancellation and numerical policy

Opposing prompts can cancel. A mean near zero has no reliable direction; the explicit lower norm bound rejects it rather than dividing by a tiny number. Grouping prompts from different classes is a schema error the function cannot infer from embeddings alone.

The same set of class prototypes can score many observations. Keep class order and prompt templates with the exported artifact so score columns retain their meaning.

## Why this matters on a robot

Words such as cup, mug or container can shift a visual classifier's behavior. Ensembling reduces some wording dependence but does not prove grounding, affordance or safe manipulation. Evaluate class and environment slices, especially when prompts describe objects absent from training.

## Questions and source

Why normalize the class mean again? Its length depends on agreement among prompts and should not become an unintended class bias. Does temperature change the winning class for a fixed image? A common positive temperature preserves order.

Source: [CLIP prompt ensembling](https://arxiv.org/abs/2103.00020). Reuse the intuition from [row normalization](/problems/clip-normalize-embeddings). No model weights or benchmark dataset are included.
