# Solution: compare paired cells under the declared tolerance

Validate exact shapes before subtracting so broadcasting cannot turn a malformed input into a plausible report. Check dtypes, finiteness, feature names, and tolerance bounds even for an empty batch.

The allowed difference is atol plus rtol times the absolute training value. Subtract serving minus training, take absolute values, and compare with strict greater-than. Equality is acceptable. Enumerate true mask locations by row and column, then map each column to its original feature name.

The output contains locations, not a blended score: averaging metres and radians would be meaningless and could hide one failing feature. A vectorized implementation uses O(ND) work and temporary space. Paired numeric agreement does not independently prove schema, frame, calibration, or timestamp correctness.
