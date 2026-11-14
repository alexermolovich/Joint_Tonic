# Solution explanation

Broadcast each episode context over its time axis, concatenate features, and mask the complete combined row. Never infer presence from zeros or broadcast across episodes. Work/output O(BT(F+C)).
