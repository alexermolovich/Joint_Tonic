# Solution explanation

Reshape contiguous columns into groups and include zero in each measured range. Divide range width by Q, clamp positive nonzero scales to float64.tiny, and use scale1 for all-zero groups. Round the zero point; separately round signed scaled weights before adding that integer zero point and clipping. Reconstruct with the matching group parameters. Work/storage O(RC). The uint8 array is an unpacked logical representation, not a packed low-bit artifact.
