# Handle local storage exhaustion without losing completed results

**Status:** Fixed locally during account persistence work. Per-scope in-memory fallback now preserves the latest drafts/results when storage throws; the UI says “Not saved to this device” and directs export. A subsequent successful write restores durable storage. Focused actual-module regression: `node --test tests/workspace-storage.test.mjs`. No GitHub issue or PR was created.

`apps/web/src/lib/local-workspace.ts:8` writes drafts, settings, solved progress, and up to 100 complete submission snapshots to one localStorage entry without handling quota errors. A valid history can exceed storage capacity before the record-count limit is reached.

## Reproduction and evidence

Verified in a fresh, headless Microsoft Edge context with no real user profile or worker jobs. The test transpiled the actual `local-workspace.ts` module with the installed TypeScript compiler and executed its exported `updateWorkspace` function in the browser. React hooks were not called.

1. Start with empty origin storage and initialize `updateWorkspace(s => s)`.
2. Create a source string of `"#" + "a".repeat(64000) + "\n"`, which is 64,002 UTF-8 bytes and below the worker's 65,536-byte source limit.
3. Append distinct completed submission objects containing that source through the real updater:

   ```js
   updateWorkspace(s => ({
     ...s,
     submissions: [job, ...s.submissions].slice(0, 100),
   }));
   ```

4. Repeat up to 100 times with unique job IDs.

Observed result on this browser:

```json
{"attemptedSubmission":82,"savedSubmissions":81,"sourceBytes":64002,"errorName":"QuotaExceededError","persistedCharacters":5204549}
```

The exact threshold varies by browser and existing draft/note size. The defect is the unhandled write failure, not a guarantee that every browser reaches the same submission count.

**Expected:** Preserve completed progress and report any storage failure clearly; bound or move bulky snapshots so valid usage cannot silently disable persistence.

**Actual:** `localStorage.setItem` throws. In `workspace.tsx`, completion stores the new submission, solved flag, and cleared active-job ID in the same update. That entire update fails. Subsequent draft/settings writes can also fail, while the workspace's saved indicator remains unconditional.

## Proposed scope and focused regression

Use a suitable store for source snapshots or an explicit byte-aware retention policy, and surface failed saves. Preserve existing data on failure. Test a near-quota workspace and a completed submission, asserting that completion does not become an uncaught storage error and that any retention/save state is accurately reported. Use isolated browser storage, not the developer's profile.
