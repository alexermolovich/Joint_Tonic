# Worked examples

### A fusible chain
For `nodes=[("x","input",None,(4,)),("a","scale","x",(4,)),("b","relu","a",(4,))]`, return `[("x",),("a","b")]`.

### A later branch blocks fusion
Appending `("c","sigmoid","a",(4,))` to that graph returns `[("x",),("a",),("b",),("c",)]`.
