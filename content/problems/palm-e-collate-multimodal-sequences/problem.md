# Collate Variable Multimodal Sequences

Different observations can produce different token counts. Padding makes one rectangular batch, but explicit lengths and presence masks must distinguish real zero-valued features from unused storage.

## Contract

`collate_multimodal(sequences,modalities)` takes two nonempty Python lists of equal length B,1<=B<=32. Each sequence is real(Li,E),0<=Li<=256, common1<=E<=128; each modality array is integer(Li,) in0..2. Return dict tokens:float64(B,Lmax,E) right-padded0, modalities:int64(B,Lmax) right-padded-1, present:bool(B,Lmax) and lengths:int64(B,). Empty examples and an all-empty batch are allowed; E remains supplied by their (0,E) shapes. No truncation or sequence sorting. The total padded token output must contain at most1,000,000 entries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Features are projected dimensionless embeddings; modality codes0image/1state/2text carry no physical units. Each example retains its supplied token order; no cross-example temporal relationship is implied. Original collator for PaLM-E-style multimodal embeddings. It does not tokenize text, encode images or insert supervision labels.


## Example 1

sequences=[[[1],[2]],[[3]]], modalities=[[0,2],[1]] returns tokens=[[[1],[2]],[[3],[0]]], modalities=[[0,2],[1,-1]], present=[[True,True],[True,False]], lengths=[2,1].

## Example 2

sequences=[empty((0,2)),[[0,0]]], modalities=[empty integer vector,[2]] returns tokens=zeros((2,1,2)), modalities=[[-1],[2]], present=[[False],[True]], lengths=[0,1]. The real zero token is present.
