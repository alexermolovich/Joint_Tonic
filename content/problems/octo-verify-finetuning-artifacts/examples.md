## Example 1

parameters=[{name:"adapter.up",shape:[2,3],trainable:True}], artifacts=[], allowed_prefixes=["adapter"], base="0"*64 returns total/trainable6, frozen0, missing_artifacts=["adapter.up"], readyFalse.

## Example 2

Adding an artifact {name:"adapter.up",shape:[2,3],base_sha256:"0"*64} clears the missing list and gives readyTrue.
