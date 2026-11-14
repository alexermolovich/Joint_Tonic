## Worked examples

**Example 1.** Use image hash `"0"*64`, encoder hash `"1"*64`, preprocessing hash `"2"*64` and shape `(4, 8)`. With cached key `None`, return the SHA-256 of the documented canonical record and `hit=False`. Reusing that returned digest as the cached key gives the same digest and `hit=True`.

**Example 2.** Change only preprocessing hash to `"3"*64` while keeping the original cached key. The new digest differs and `hit=False`; unchanged image bytes alone are insufficient.
