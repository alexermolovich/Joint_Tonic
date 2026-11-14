# Account workspace persistence

## Behavior

Signed-out learning continues in the original `joint-tonic.workspace.v1` browser workspace. Signing in opens a separate cache keyed by the verified account's SDK identity; guest drafts, notes, bookmarks and solved flags are never imported automatically. Auth changes remount the workspace, cancel old requests and invalidate callbacks. Server data is accepted only when its owner matches the active account. Pending edits stay local if the network or database is unavailable.

Signed-in drafts and Markdown notes are saved per immutable problem version. Bookmarks identify a problem. A version change archives old local text for export in Settings instead of putting it into the new contract. A successful account fetch supplies authoritative solved progress and the latest 100 submission snapshots. Account job IDs cached on this device remain resumable until polling reports completion; cross-device active-job discovery requires the evaluator to publish queued/running job rows.

Account and guest caches are browser storage, not encrypted storage. Reset browser cache removes only the active local cache, including unsynced edits; it does not delete account records. Signing out restores the guest workspace. Settings exposes sync status, retry, conflict choices, preserved older-version text and JSON export.

## Editable records and conflicts

`GET /api/workspace` returns `{ownerId, items, versions, solved, submissions, activeJobs}` with `Cache-Control: private, no-store`. Each item has `{kind, slug, version, body, revision}`. `PATCH` accepts exactly `{kind, slug, version, body, expectedRevision}` for `draft`, `note`, or `bookmark`. It rejects fields claiming an owner, score, submission or solved state. Text is bounded to 100,000 UTF-8 bytes. Bookmark bodies are `"1"` or `"0"`.

Both routes validate the bearer with Supabase `auth.getUser(accessToken)` and issue database requests under that same token, preserving owner-only RLS. UUID browser workspace IDs confer no authenticated authority. Errors carry a correlation ID; logs include event/type/count metadata and never learner text, tokens or email.

The `save_workspace_item` RPC is a security-invoker function with no user-ID argument. It creates revision 1 or locks the owner's existing row and compares the expected revision. On a mismatch it returns HTTP 409 with the account text and revision. Empty text and false bookmarks are revisioned tombstones. The browser retains both versions and requires an explicit “Use account version” or “Keep this device’s version” choice. A save acknowledgment never discards an edit typed while the save was in flight.

The client checks for changes on focus, network reconnection and every 30 seconds while visible. Debounced edits are serialized through one sync loop. A clean open editor receives remote text; an unsaved local editor is not overwritten. All-missing or unavailable account storage leaves local editing usable after the initial bounded request fails.

## Trusted submission persistence

Only the evaluator control plane can execute `record_evaluation(p_job)`; `public`, `anon` and `authenticated` cannot. The service-role RPC atomically inserts a terminal job, its Submit evaluation, and its first verified solve. Public Runs never create scored submissions. Failed Submit and platform-error results remain inspectable but do not create progress.

The envelope contains `id`, `user_id`, `slug`, `version`, `mode`, terminal `status`, `code`, `created_at`, `started_at`, `finished_at`, `result`, and `lineage`. Result includes safe test summaries, a Boolean aggregate verdict and `duration_ms`. Lineage requires `grading_protocol: "data-only-functions-v1"`, `evaluator_sha256`, `fixture_sha256`, `runtime_image_digest` and integer `seed`. Both evaluator and fixture hashes identify the exact raw authored `cases.py` bytes in this runtime. The actual OCI digest and both hashes must match the published catalog version.

The RPC verifies the aggregate verdict against the trusted test summaries. Its inputs are trusted control-plane outputs, not cryptographic proof: the isolated data-only grader must establish the result before invoking it. The worker posts `{p_job}` to the control plane's `/api/evaluations`, authenticated with `WORKER_SERVICE_TOKEN`; only the control plane holds the server-only Supabase key and invokes the RPC. The worker, browser, learner process and learner filesystem have no database service key. Same-ID retries are accepted only if the immutable owner, content, source, timestamps and result match. All derived records are in the same transaction.

## Provisioning and remaining deployment requirements

All four migrations through `20261114040000_catalog_without_execution.sql` were applied to the authorized hosted project on 2026-11-14. CLI migration history confirms the remote versions. Anonymous REST smoke checks returned the public catalog successfully and denied private draft reads and trusted evaluation RPC calls. The Linux execution host has not been selected.

Browser draft/note/bookmark sync can start before evaluator hosting. Publish immutable catalog-only rows with null `runtime_image_digest` and explicit `metadata.grading_protocol: "unavailable"`. The database constraint rejects missing/null protocol declarations and execution protocols without an image. The trusted evaluation RPC rejects these catalog-only rows even for a service-role caller. A later qualified execution identity requires a new semantic version; existing published rows are never silently upgraded.

For catalog-only publication using the already authenticated CLI, without extracting a service credential:

```text
node scripts/check-evaluator-hashes.mjs
node scripts/sync-supabase-catalog.mjs --catalog-only --prepare-cli-seed
npx supabase --workdir .local/supabase-catalog-publish link --project-ref <authorized-project-ref>
npx supabase --workdir .local/supabase-catalog-publish db push --include-seed --dry-run
npx supabase --workdir .local/supabase-catalog-publish db push --include-seed --yes
```

The generated workspace and seed stay under ignored `.local/`; the normal local Supabase configuration remains unchanged. Review the plan and dry run before application. The seed is one transaction, accepts idempotent matching versions and rejects any immutable identity conflict. It includes public metadata and hashes, never hidden test contents or reference solutions. Source text must be valid UTF-8 and evaluator bytes canonical LF.

Production execution remains a separate sequence:

1. Keep the intended project linked through the user's normal CLI authentication. Review future migration diffs before applying them.
2. Build and qualify the isolated worker image. Obtain its actual immutable OCI digest; never invent a placeholder. Production eligibility requires a reviewed `execution_contract` with protocol `data-only-functions-v1`, semantics `value-only`, and a nonempty `reviewed_by`. Existing native problems are not automatically qualified: mutation, aliasing, dtype/device and autograd contracts need a compatible verified execution boundary. Catalog metadata otherwise records `native-local-v1`.
3. Prepare a catalog plan with `node scripts/sync-supabase-catalog.mjs --runtime-image-digest=sha256:<actual-built-digest>`. It writes `.local/supabase-catalog-plan.json` and performs no remote mutation by default.
4. Once approved for application, use the same command with `--apply` and server-only `SUPABASE_URL` plus `SUPABASE_SECRET_KEY` or `SUPABASE_SERVICE_ROLE_KEY`. Existing immutable versions are checked, never silently replaced. A mismatching content/evaluator/image identity requires a reviewed new semantic version. Catalog publication alone does not qualify a problem for production execution; the worker must enforce its qualification allowlist.
5. Configure a fresh server-only Supabase persistence key on the control plane, and the worker's image digest, `CONTROL_PLANE_URL` and shared `WORKER_SERVICE_TOKEN` on the chosen host. Do not reuse any historically pasted secret. The web workspace API itself needs only its public Supabase key and user bearer tokens.

## Verification

Focused commands:

```powershell
npm run typecheck
node --experimental-strip-types --test tests/workspace-cache.test.ts tests/workspace-auth.test.mjs
node --test tests/workspace-sync-ui.test.mjs
npm exec supabase -- test db
```

The browser test uses mocked Auth/workspace responses and isolated contexts; it does not create hosted users or upload work. It covers guest/account separation, save/reload, remote updates, offline conflicts, sign-out and a second account.

Where Docker/PostgreSQL is unavailable, a temporary embedded PostgreSQL check is reproducible without changing application dependencies:

```powershell
npm install --prefix .local/persistence-db-test --no-save --package-lock=false @electric-sql/pglite@0.5.16
node scripts/check-persistence-sql.mjs
```

That check executes all migrations and 49 SQL assertions using actual PostgreSQL roles, RLS and PL/pgSQL, with minimal Supabase Auth stubs and local assertion wrappers. It also verifies generated catalog insertion, idempotent retry, literal text handling and immutable-conflict rejection. It is not the pgTAP extension itself. All four hosted migrations and 321 catalog-only versions were applied and verified on 2026-11-14. Each remote version matches its planned content/evaluator identity; anonymous catalog reads succeed while drafts and the trusted evaluation RPC reject anonymous access. These are separate hosted checks; live signed-in persistence, email delivery, actual OCI image publication and a deployed evaluator need their own evidence.

References: [Supabase getUser](https://supabase.com/docs/reference/javascript/auth-getuser), [database functions and privileges](https://supabase.com/docs/guides/database/functions).
