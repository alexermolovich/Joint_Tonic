## Approach

Validate exact record fields, semantic versions and lowercase SHA256 strings, sort records, serialize deterministically and hash the resulting UTF-8 bytes.

O(G log G + serialized bytes) time and O(serialized bytes) space for G records.
