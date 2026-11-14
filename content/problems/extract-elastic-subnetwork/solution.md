# Solution explanation

Validate every layer, including those outside the requested depth. For each retained layer take the leading output/input channels and the centered odd spatial crop, then copy. Independent copies are necessary even when input layers alias. Validation O(L C² K²), output work/storage O(depth width² kernel²).
