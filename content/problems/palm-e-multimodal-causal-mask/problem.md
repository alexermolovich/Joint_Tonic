# Build a Multimodal Causal Attention Mask

Putting sensors into a language sequence must not let a prediction read future tokens. A padding or missing-sensor token should be neither a source of information nor an active query.

## Contract

`multimodal_causal_mask(modalities,present)` receives integer modalities(L,) with IDs0=image,1=state,2=text,0<=L<=256, and present:bool(B,L),1<=B<=16. Return bool(B,L,L), True means query row i may read key column j exactly when i>=j and both tokens are present in that batch. Modalities validate the token schema but do not override causality. Missing query rows are entirely false, including diagonal. Empty L is allowed; no special always-visible token is added.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

All axes are token positions and dimensionless modality identifiers; no actuator units. Sequence order defines causality. Tokens may describe multiple sensors but callers must synchronize them before this function. Original dense causal-mask component for a PaLM-E-style interleaved sequence. This declares ordinary autoregressive causality, not bidirectional vision blocks or a full model attention implementation.


## Example 1

modalities=[0,1,2], present=[[True,False,True]] returns [[[True,False,False],[False,False,False],[True,False,True]]].

## Example 2

modalities=[2], present=[[False],[True]] returns [[[False]],[[True]]]. Presence varies by batch, even for one shared modality sequence.
