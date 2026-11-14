# Validate a Robot Dataset Datasheet

## Contract

`validate_robot_datasheet(document) -> list[tuple[str, str]]`. document must be a Python dict with at most 32 string keys (each1..64 chars); otherwise raise ValueError. Required text fields are dataset_id, version, motivation, collection_method, calibration_sha256, license, maintenance, limitations. Required list fields are embodiments, sensors, tasks, intended_uses, prohibited_uses. Extra keys each produce(key,"unexpected"). Absent required fields each produce(key,"missing").

Present text fields must be str of 1..1024 characters after strip; otherwise report invalid. Stripping is used only to check text nonemptiness and length; ID, version and digest syntax are checked on the original string with ASCII digits. dataset_id must additionally match the common ID rule; version must contain exactly three decimal integer components separated by literal dots, each component in 0..9999 and no leading zeros except0; calibration_sha256 must be a valid digest. A literal string"unknown" is permitted only for calibration_sha256 or license and produces unknown instead of invalid. Lists must be Python lists of0..128 unique common IDs; embodiments, sensors, tasks, intended_uses must be nonempty, prohibited_uses may be empty. Any malformed list yields one invalid issue at its field, not per-item issues. Return tuples sorted lexically, at most one issue per present field. Do not infer actual consent, rights or quality from completeness. This one schema task also implements missing provenance detection.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

A complete document has dataset_id="fr3_set", version="1.0.0", motivation="pick blocks", collection_method="teleoperation", calibration_sha256="1"*64, license="CC0-1.0", maintenance="lab", limitations="one room", embodiments=["fr3"], sensors=["wrist_rgb"], tasks=["pick"], intended_uses=["research"], prohibited_uses=[]. Its report is[].

Starting from that document, delete license, set calibration_sha256="unknown", and add extras=1. Report[("calibration_sha256","unknown"),("extras","unexpected"),("license","missing")].

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
