# Generate a Data-Use Risk Report

## Contract

`data_use_review_flags(datasets, requested_use, requested_embodiment) -> list[dict]`. datasets is a list of 0..10000 exact records {dataset_id, intended_uses, prohibited_uses, embodiments, contains_personal_data, consent, license_known}; IDs unique. Each of the three lists contains 0..128 unique common IDs; both scalar requests are common IDs. contains_personal_data and license_known are bool; consent is"granted","denied" or"unknown". Both intended and prohibited may contain the same use: the request still triggers prohibited_use. Do not add a separate contradiction flag; outside_intended_use applies only when the request is absent from intended.

For each dataset emit sorted flags from: prohibited_use if request is prohibited; outside_intended_use if request is absent from intended; unsupported_embodiment if absent from embodiments; unknown_license if license_known=False; consent_denied or consent_unknown only when contains_personal_data=True and the corresponding consent value is declared. Return exact rows{dataset_id, flags, needs_review}, sorted by dataset_id, where needs_review=bool(flags). Empty flag lists mean only that these declared rules found no mismatch, not legal permission, verified consent or fitness. No policy facts are inferred from a person's identity.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

Dataset a:intended[research], prohibited[commercial], embodiments[fr3], contains_personal_data=False, consent="unknown", license_known=True. Request research/fr3 gives flags[], needs_review=False.

With personal_data=True, consent="unknown", license_known=False and request commercial/panda, flags are["consent_unknown","outside_intended_use","prohibited_use","unknown_license","unsupported_embodiment"], needs_review=True.

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
