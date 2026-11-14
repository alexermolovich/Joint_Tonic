## Worked examples

**Example 1.** One image token `[1]` and two text tokens `[0]`, `[0]`, all valid: image weights `[.5,.5]`, image context `[0]`; each text query has weight `[1]` and context `[1]`.

**Example 2.** Make both text tokens invalid. Image queries have no valid keys and text queries are invalid; every returned context and weight is zero, without NaNs.
