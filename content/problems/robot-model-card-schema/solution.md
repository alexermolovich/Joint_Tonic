# Solution explanation

Validate the complete model/artifact header and every metric record. Track measured slices, flag zero denominators and impossible success counts independently, then report required slices that were not measured. Preserve low but valid success rates rather than inventing a release threshold. Work O(M+S+I log I), storage O(M+S+I).
