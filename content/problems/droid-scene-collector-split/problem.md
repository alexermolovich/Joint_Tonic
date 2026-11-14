# Split Demonstrations by Scene and Collector

## Contract

`split_scene_collector_components(episodes, held_out_scenes) -> dict`. episodes is a list of 0..10000 exact {episode_id, scene_id, collector_id} records with unique episode IDs; held_out_scenes is a list of 0..10000 unique declared scene IDs. Empty episodes require empty held-out scenes. Join episodes sharing a scene OR a collector; take the transitive closure. A component goes to test if any episode in it has a held-out scene; all other components go to train. Return train_ids and test_ids sorted lists plus component_ids mapping every episode_id to the lexically smallest episode_id in its connected component. This is deterministic group isolation, not a random proportional split or the dataset's published benchmark split. Work near-linear union/find plus sorting; preserve inputs.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

episodes a(s1, c1), b(s2, c1), c(s2, c2), d(s3, c3), held_out_scenes=[s1] gives test_ids[a, b, c], train_ids[d], component_ids{a:a, b:a, c:a, d:d}. Collector and scene links propagate transitively.

For a(s1, c1), b(s2, c2) and held_out_scenes=[], train_ids=[a, b], test_ids=[], component_ids{a:a, b:b}.

## Source and scope

Original bounded component inspired by [2024-droid](https://arxiv.org/abs/2403.12945). It does not reproduce the full paper or establish hardware safety or data-use authorization.
