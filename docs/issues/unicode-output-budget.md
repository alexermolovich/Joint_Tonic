# Do not count JSON escaping as excess learner output

**Status:** Local issue draft. No GitHub issue was created; the existing remote publishing block remains in effect.

The evaluator rejects some output below its documented 64 KiB learner-output limit because the final report expands Unicode during JSON serialization. `harness.py:73` uses the default `json.dumps` ASCII escaping; `server.py:85` then applies the 65,536-byte transport cap to the serialized report.

## Reproduction and evidence

Verified through two direct calls to the real WSL bubblewrap `sandbox` function. The live HTTP worker, repository problem files, and job history were not changed.

Import `apps/worker/server.py`, read `content/problems/se3-transform-points/reference.py`, and evaluate these two source variants with `sandbox(source, "se3-transform-points", "run")`:

```python
# Variant A: 44,001 UTF-8 bytes including the newline.
source = reference + "\nprint(chr(0x1F642) * 11000)\n"

# Variant B: equal-size ASCII output, also 44,001 UTF-8 bytes.
source = reference + "\nprint('a' * 44000)\n"
```

| Variant | Learner output | Actual result |
|---|---:|---|
| A: Unicode | 44,001 UTF-8 bytes | `passed: false`, `failure_category: learner-output-limit`, zero reported tests |
| B: ASCII control | 44,001 UTF-8 bytes | `passed: true`, all three public tests pass |

Variant A returns `Output exceeded 64 KB. Reduce print output.` Each emoji occupies four UTF-8 bytes but becomes a twelve-byte escaped surrogate pair in the JSON envelope. The retained log therefore expands beyond the transport cap even though learner output is below its limit. Variant B retains 16,384 log characters and completes normally.

**Expected:** These equal-byte outputs receive the same learner-output-budget treatment, with bounded diagnostics and a valid result report.

**Actual:** A correct reference solution is classified as a learner output-limit failure solely because its diagnostics use Unicode.

## Proposed scope and focused regression

Keep the learner-output budget separate from bounded report serialization. Ensure diagnostic retention is byte-aware and reserve enough transport space for test metadata and the final result. UTF-8 JSON output may reduce escaping overhead, but the entire report must still have an explicit bound.

Add focused Unicode and ASCII controls using the real isolated runner, plus an over-budget case that must still fail. Do not relax the raw descriptor-output or resource boundaries.
