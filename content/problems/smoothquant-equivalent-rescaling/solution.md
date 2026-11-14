# Solution explanation

Validate that every scale is positive and within bounds, then divide each activation column and multiply its corresponding weight row. Promote float32 inputs before arithmetic, preventing low-precision intermediates from underflowing before the declared float64 calculation. The diagonal factors cancel in the unquantized linear product. Work and output storage O(NC+CD).
