# Interleave Image, State, and Text Tokens

A language model can consume image, state and text embeddings in one sequence when they share a feature width. An explicit layout makes the sequence order testable instead of hiding it inside string replacement or concatenation conventions.

## Contract

`interleave_modal_tokens(image,state,text,layout)` receives three real matrices (Ni,E),(Ns,E),(Nt,E), 0<=eachN<=512, common1<=E<=128; layout integer(L,2),0<=L<=1024. Each row contains (kind,index): kind0=image,1=state,2=text; index must address that source. Return (tokens:float64(L,E), modalities:int64(L,)). Preserve layout order and permit repeated source rows. Empty layout returns correctly shaped empty outputs. Empty source is allowed only when no layout row addresses it. No padding, projection, positional embeddings or automatic special token is inserted.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Projected token features are dimensionless; IDs are indices, not physical channels. All source arrays belong to one caller-aligned observation context; ordering is supplied, not inferred from timestamps. Original explicit interleaver motivated by PaLM-E embedding continuous observations into a language stream. It assumes the sensor projections and tokenizer already ran.


## Example 1

image=[[1,2]], state=[[3,4]], text=[[5,6]], layout=[[2,0],[0,0],[1,0]] returns tokens=[[5,6],[1,2],[3,4]], modalities=[2,0,1].

## Example 2

image=[[7]], state=empty((0,1)), text=empty((0,1)), layout=[[0,0],[0,0]] returns [[7],[7]] and [0,0]. Repetition is intentional, not deduplicated.
