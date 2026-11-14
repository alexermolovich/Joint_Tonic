# Solution

Validate color ranges, sorted metric depths and the complete weight-plus-background mass. RGB is a direct weighted sum including background. Foreground depth is the sample-depth moment divided by foreground mass only where that mass exceeds the documented threshold. Fill other depths with NaN and expose validity separately. No weight renormalization is applied to color. Time and output/intermediate storage are O(RS).
