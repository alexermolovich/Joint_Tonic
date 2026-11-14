# Verify Trainable Parameters and Fine-Tuning Artifacts

A fine-tuning artifact should contain exactly the learned parameter subset and identify the frozen model it extends. Counting trainable entries, checking namespace boundaries and matching base hashes catch different ways a seemingly valid checkpoint can be incomplete.

## Contract

parameters list<=256 of exact dicts name:str,shape:list of1..4 built-in positive ints<=10000,trainable:bool; product(shape)<=1e9, names unique ASCII dotted identifiers<=80chars. artifacts list<=256 exact dicts name:str,shape:list,base_sha256:str; names unique and must occur in parameters with identical shape. allowed_prefixes nonempty list<=16 unique dotted identifiers; matching means name==prefix or name starts prefix+dot (never raw textual prefix). base_sha256 exactly64lowercasehex. Return total_count int, trainable_count int, frozen_count int, unexpected_trainable sorted names, missing_artifacts sorted TRAINABLE names absent from artifacts, frozen_artifacts sorted supplied FROZEN names, mismatched_base sorted artifact names whose well-formed hash differs, and ready bool true iff all four lists empty. Unexpected trainability or differing valid hash are reported, not raised. Malformed structures/unknown artifacts/mismatched shape raise ValueError. Empty parameter list is allowed and ready if artifacts empty.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original deterministic artifact audit motivated by Octo adaptation and reproducibility; no weights are loaded, trained or serialized by this function.


## Example 1

parameters=[{name:"adapter.up",shape:[2,3],trainable:True}], artifacts=[], allowed_prefixes=["adapter"], base="0"*64 returns total/trainable6, frozen0, missing_artifacts=["adapter.up"], readyFalse.

## Example 2

Adding an artifact {name:"adapter.up",shape:[2,3],base_sha256:"0"*64} clears the missing list and gives readyTrue.
