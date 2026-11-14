## Worked examples

**Example 1.** One query has logits `[0, 0]` (foreground, background), box `[.5,.5, 1, 1]`, no padding and threshold `.5`. Output: box `[0, 0, 1, 1]`, score `.5`, label `0`, valid `True`.

**Example 2.** Use the same input with threshold `.6`. Output: box `[0, 0, 0, 0]`, score `0`, label `-1`, valid `False`.
