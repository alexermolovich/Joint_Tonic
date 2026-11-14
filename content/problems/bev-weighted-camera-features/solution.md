# Solution

Zero invalid weights and find the maximum remaining weight per query. Divide by that maximum before normalization: this preserves the mathematical mean while preventing very small positive weights from underflowing when multiplied by features. Normalize over camera and sample axes, then reduce weighted features over the same axes. Queries with no positive mass return zeros and false. Time and temporary storage are O(BQCSD).
