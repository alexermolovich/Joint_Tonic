# Mask Unavailable Action Dimensions

Implement mask_action_dimensions(actions: np.ndarray, available: np.ndarray) -> np.ndarray.

actions is NumPy float64 shape(B,D),0<=B<=1024,1<=D<=128. available is NumPy bool with exactly the same shape. A true mask entry means the channel is present under that batch item's declared embodiment contract. Each available action value must be finite with absolute value<=1e6. Unavailable values may be any float64, including NaN or infinity; they are placeholders and must not be inspected as physical actions.

Return a fresh float64 array(B,D): copy each available value and put exact0.0 at every unavailable position. All-false rows and an empty batch are valid. Preserve both inputs, support noncontiguous arrays and avoid storage aliasing. Every malformed type, dtype, shape, bound or invalid available value raises ValueError.

Channel meanings, units, frames and position/delta conventions remain upstream metadata and may differ across batch rows. This operation does not make channels physically equivalent. Retain the original availability mask for downstream losses: returned zeros do not distinguish unavailable channels from valid zero actions. No loss reduction, denormalization, RNG or hardware execution occurs.

## Worked examples

### Different supported channels

~~~python
mask_action_dimensions(np.array([[1.,2.,3.],[4.,5.,6.]]),
                       np.array([[True,False,True],[False,True,False]]))
# [[1.,0.,3.],[0.,5.,0.]]
~~~

Only the supplied mask decides which values survive.

### Invalid placeholders are removed safely

~~~python
mask_action_dimensions(np.array([[np.nan,0.,np.inf]]),
                       np.array([[False,True,False]]))
# [[0.,0.,0.]]
~~~

The middle zero is a valid action. The other zeros replace unavailable values. Multiplication by a zero mask would leave NaN from the placeholders.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864).

