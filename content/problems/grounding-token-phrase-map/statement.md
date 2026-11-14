# Map Text Tokens to Grounded Phrases

Implement `phrase_token_map(token_offsets: np.ndarray, phrase_spans: np.ndarray, text_length: int) -> np.ndarray`.

Map character spans to tokens with an explicit half-open overlap rule.
token_offsets int64 (T,2) and phrase_spans int64 (P,2) store [start,end) character offsets into the same original string,0<=T,P<=4096. text_length is a built-in int 0..1000000, not bool. Tokens may have empty offsets [a,a), representing special/padding tokens; phrases must be nonempty. All bounds satisfy 0<=start<=end<=text_length. Return bool (P,T), true for positive-length token/phrase intersection: max(starts)<min(ends). Preserve order, allow overlapping phrases and unsorted offsets, and permit all-false rows when tokenization provides no coverage. Offsets are Unicode code-point indices supplied by the caller, not bytes. This is an original deterministic alignment contract; no tokenizer or phrase parser runs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Tokens `[[0,0],[0,3],[4,7],[8,11]]`, phrase `[4,11)`, text_length=11 gives `[False,False,True,True]`.
2. Token `[2,5)` overlaps phrase `[4,6)` but not phrase `[5,6)`: touching at a half-open endpoint has zero overlap.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
