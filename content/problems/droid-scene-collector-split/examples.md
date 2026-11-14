# Worked examples

episodes a(s1, c1), b(s2, c1), c(s2, c2), d(s3, c3), held_out_scenes=[s1] gives test_ids[a, b, c], train_ids[d], component_ids{a:a, b:a, c:a, d:d}. Collector and scene links propagate transitively.

For a(s1, c1), b(s2, c2) and held_out_scenes=[], train_ids=[a, b], test_ids=[], component_ids{a:a, b:b}.
