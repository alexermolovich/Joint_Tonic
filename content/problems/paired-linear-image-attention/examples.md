# Worked examples

1. With all four weight matrices zero, outputs equal the supplied feature rows wherever valid and are zero elsewhere. The messages are zero.
2. D=1, all four weights 1, one valid source feature `[[1.]]`, one valid target feature `[[2.]]`: self_source is `[[2.]]`, self_target `[[4.]]`, and both final outputs are `[[6.]]`. Sequentially updating the target from an already updated source would be wrong.
