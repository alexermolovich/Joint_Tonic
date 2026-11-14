# Worked examples

### Example 1

tasks a(pick,cup,tray,kitchen),b(pick,cup,tray,lab),c(place,cup,tray,kitchen) -> group(pick,cup,tray):tasks[a,b],scenes[kitchen,lab],True; group(place,cup,tray):tasks[c],scenes[kitchen],False.

### Example 2

Two tasks a,b both(pick,cup,tray,kitchen) -> one group,task_ids[a,b],scene_ids[kitchen],has_scene_variationFalse.
