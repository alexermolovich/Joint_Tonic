# Solution explanation

Validate shapes and dtypes, then inspect only values selected by availability. Use selection, not multiplication: NaN times zero is still NaN. A fresh zero-filled output populated at true entries preserves exactly the available values. Work and output storage are O(BD).
