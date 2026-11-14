## Worked examples

**Example 1.** With every dimension equal to 1, image `.5`, proprioception `2`, vision weight `3`, proprioception weight `4`, bias `1` and both masks true, return tokens `[[[10.5]]]`, flat `[[10.5]]` and used `[[True]]`.

**Example 2.** Keep the same data but mark proprioception invalid. Return tokens `[[[0]]]`, flat `[[0]]` and used `[[False]]`. A valid zero pixel would not itself invalidate the slot.
