# Solution explanation

Form each candidate weight delta and report its mean squared entries. Multiply the whole calibration matrix by that delta before squaring, preserving correlations between channels. Average output error over tokens and output channels, then choose the first minimum in candidate order. Work O(KNCD), intermediate storage O(KCD+KND). Ranking by weight MSE implements a different objective.
