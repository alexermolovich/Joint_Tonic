# Worked cases

### Case1: one visual block followed by action slots

```text
steps=1, visual_tokens=2, action_tokens=2
slot labels: [V0.0,V0.1,A0.0,A0.1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,1,0,0],
 [1,1,0,0],
 [1,1,0,0]]
```

The second visual query sees the first visual key and itself. Both action queries see both visual keys, but neither sees action keys.

### Case2: a later visual query can see an earlier placeholder

```text
steps=2, visual_tokens=1, action_tokens=1
slot labels: [V0,A0,V1,A1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,0,0,0],
 [1,1,1,0],
 [1,0,1,0]]
```

The row for V1 includes A0. The row for A1 excludes A0 and A1. This is intentional reference behavior; replacing every action-key column with zeros would produce a different mask.

## Additional public edge case

rt1_attention_mask(True,1,1) raises TypeError; rt1_attention_mask(1,0,1) raises ValueError. The minimal valid call(1,1,1) returns[[True,False],[True,False]].

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
