# Validate a Model Card Schema

## Contract

`validate_robot_model_card(card, required_slices) -> list[tuple[str, str]]`. card must be a dict with exactly model_id, artifacts, intended_embodiments, limitations, metrics; malformed structure raises ValueError. model_id is a common ID. artifacts is an exact dict weights, preprocessing, action_decoder, runtime, each a valid SHA256. intended_embodiments is a list of 1..128 unique common IDs. limitations is a str of 1..4096 chars after strip. required_slices is a list of 0..256 unique common IDs.

metrics is a list of 0..10000 exact{slice_id, trials, successes} records with unique slice IDs, trials/successes built-in ints in 0..10^9. Counts success>trials are permitted anomaly evidence. All referenced slice IDs follow the ID rule; extra measured slices are allowed. Return(slice_id,"missing") for each required unmeasured slice; for every measured slice independently report no_trials if trials==0 and invalid_success_count if successes>trials. Sort tuples lexically. A structurally valid card with complete nonzero counts returns[], even if success rate is low: this is reporting completeness, not a performance gate. All identities are supplied commitments, not verified artifact bytes.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

For both examples, the complete header is model_id="policy", artifacts={weights:"1"*64, preprocessing:"2"*64, action_decoder:"3"*64, runtime:"4"*64}, intended_embodiments=["fr3"], limitations="One room only". Add the metrics field specified below.

With valid model/artifact/embodiment/limitations fields and metrics=[{slice_id:"day", trials:10, successes:2}], required_slices=["day"] yields[]. Low performance is reported, not hidden by a schema error.

Same valid header, metrics=[{slice_id:"night", trials:0, successes:1}], required_slices=["day","night"] yields[("day","missing"),("night","invalid_success_count"),("night","no_trials")].

## Source and scope

Original bounded component inspired by [2018-model-cards](https://arxiv.org/abs/1810.03993). It does not reproduce the full paper or establish hardware safety or data-use authorization.
