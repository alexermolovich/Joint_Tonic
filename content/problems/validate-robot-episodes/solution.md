# Solution approach

Validate the schema first so a malformed rule is a caller error rather than an alleged dataset anomaly. Iterate episodes and preserve the episode index in every issue. Check the timestamp container before indexing it, then check values and adjacent order.

For each declared signal, handle presence and metadata, validate the values container and time length, count None rows, and inspect each nonmissing row. Convert the row to a NumPy array to inspect shape and dtype. Check shape first; if shape is valid, check the allowed dtype kinds. Check finiteness before inclusive min/max bounds. Emit only one of shape/dtype/nonfinite/range for each row.

Check unexpected signals independently when requested. Finally sort issues by episode, path and code. This avoids dependence on dictionary insertion order.

Time is O(total scalar values + issues×log(issues)); the result uses O(issues) memory plus one temporary row array. No schema inference, resampling, physical conversion or automatic repair occurs.
