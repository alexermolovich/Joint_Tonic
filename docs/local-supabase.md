# Local Supabase persistence

Login and account workspaces are implemented. See [Supabase Auth](supabase-auth.md) and [account workspace persistence](../specs/account-workspace-persistence.md) for the API, account isolation, conflict handling and deployment prerequisites.

Without database configuration, signed-out drafts, notes and progress remain in the original browser workspace. Signed-in caches are separate and preserve pending edits while storage is unavailable. Cloud synchronization needs the checked-in migrations and a published immutable catalog. No hosted migrations or catalog rows have been applied by this implementation.

## Start the local stack

Requirements: Node.js matching the repository, installed npm dependencies, and a running Docker-compatible daemon. Docker Desktop on Windows normally supplies the daemon. A docker executable alone is insufficient.

From the repository root:

~~~powershell
npm install
npm exec supabase -- start
npm exec supabase -- status
~~~

The repository pins Supabase CLI 2.58.5. Do not run supabase init again: config.toml is checked in. The first start can download Supabase container images. Start is a deliberate setup step for a developer; it has not been run as part of authoring this migration.

With this config, the local services use:

| Service | Address |
|---|---|
| API/Auth/REST/Storage gateway | http://127.0.0.1:54321 |
| PostgreSQL | 127.0.0.1:54322 |
| Studio | http://127.0.0.1:54323 |
| Local email inbox | http://127.0.0.1:54324 |

The local Auth site URL is http://127.0.0.1:3000, with http://localhost:3000 also allowed. Email confirmation is disabled for local development. Edge functions and analytics are disabled to keep this local stack smaller.

If start reports a daemon connection error, start the Docker runtime and retry. The web app's current localStorage/file-backed mode continues to work without Supabase.

## Optional browser configuration

Use the values printed by your own local CLI:

~~~powershell
npm exec supabase -- status --output env
~~~

CLI 2.58.x exposes API_URL and ANON_KEY in its environment output. It can also show SERVICE_ROLE_KEY, DB_URL and JWT_SECRET. Exact display labels vary by CLI version; use the local anonymous/public client key, not the service-role or secret key.

Set these values in apps/web/.env.local using the API_URL and ANON_KEY from that local status output:

~~~dotenv
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<local ANON_KEY from supabase status>
~~~

The helper also accepts NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY instead of the legacy ANON_KEY when your local CLI supplies a publishable client key. Never place SERVICE_ROLE_KEY, JWT_SECRET, database passwords or secret API keys in a NEXT_PUBLIC_ variable. Restart the Next.js development server after changing its public environment.

~~~typescript
import { getSupabaseBrowserClient } from "@/lib/supabase";

const client = getSupabaseBrowserClient();
if (client) {
  const { data, error } = await client.auth.getUser();
}
~~~

getSupabaseBrowserClient returns null on the server, when configuration is absent/invalid, for non-loopback HTTP, or for a secret key. The cached client uses real @supabase/supabase-js auth/session handling. Hosted HTTPS Auth is the authorized exception to the local development boundary.

## Apply or reset migrations locally

A fresh supabase start applies the migration set during database initialization. To apply pending migrations to an existing running local database without resetting it:

~~~powershell
npm exec supabase -- migration up --local
~~~

To recreate the local database and replay every migration:

~~~powershell
npm exec supabase -- db reset --local
~~~

Reset deletes application rows and local Auth users from that local database. Export anything you want to retain first. It does not clear browser localStorage or .local/jobs, which belong to the current separate adapters.

To stop containers while preserving local development data:

~~~powershell
npm exec supabase -- stop
~~~

Do not add --no-backup unless discarding local data is intentional. No login, link, remote db push or Vercel deployment is required for this workflow.

## Schema contract

| Table | Purpose | Browser permissions |
|---|---|---|
| profiles | Private display name keyed by auth.users.id | Read/insert/update own row |
| problems | Stable slug identity | Read only when a published version exists |
| problem_versions | Semantic version, catalog metadata, content hash, evaluator/runtime provenance | Read published/retired versions |
| drafts | Mutable code per user and immutable problem version | CRUD own rows |
| notes | Private Markdown per user and version | CRUD own rows |
| jobs | Frozen source snapshot, mode, correlation/idempotency keys, lifecycle | Enqueue own queued jobs and read own jobs |
| submissions | Immutable link from owner/version to a submit job | Read own records |
| evaluations | Immutable verdict, test totals and pinned evaluator/runtime/fixture evidence | Read through own submission |
| progress | Verified first passing submission per user/version | Read own records |
| bookmarks | Saved stable problems | CRUD own rows |

All API-visible tables enable RLS. Private policies use auth.uid(), not the browser's local workspace UUID. Browser roles cannot update jobs, write evaluations, mark a problem solved or alter published content. A trusted server/controller persists verified results.

Published problem versions require an image digest and content hash. Publication freezes metadata and evaluation provenance; retirement can change only state. Fixes create a new semantic version. Current host-run content remains repository content until an ingestion adapter creates properly versioned database rows.

Jobs transition queued → running → completed/failed/cancelled, or queued → cancelled. A failed test is normally a completed job with a failed verdict; failed job status describes an execution/platform failure. A terminal job cannot be updated. Job source, owner, mode, version and identity are frozen from creation.

A submission must reference a submit job owned by that same user and problem version. An evaluation can only be inserted once per submission. Corrections use a new job/submission rather than editing historical evidence. Progress requires an existing passing evaluation for the same owned submission/version. Foreign keys protect history from catalog deletion. Account deletion may cascade private learner records through auth.users.

Evaluation summaries and job results must contain learner-safe bounded metadata only. Hidden test input, reference code and secrets belong outside public database payloads. Storage buckets and Realtime publications are intentionally not enabled by this schema; add narrowly scoped artifact policies and chosen-table publications with their adapters later.

## Migration from the current local mode

1. Add authenticated session handling in the Next.js control plane and verify Supabase user identity server-side. The current random workspace UUID is not an Auth identity.
2. Add a trusted content-ingestion adapter that imports metadata/hashes and pinned evaluator/runtime versions from content/problems. Do not import hidden tests or reference code into public metadata.
3. Replace localStorage draft/note/bookmark reads and writes with owner-scoped queries. Offer an explicit one-time import of local drafts after sign-in; retain a local fallback during transient errors.
4. Replace .local/jobs persistence with an API/controller adapter. Queue and claim jobs transactionally; use FOR UPDATE SKIP LOCKED for the claim operation. The separate isolated evaluator receives only the narrow job payload, never service-role/database credentials.
5. Persist each submit job, immutable submission and evaluation in a transaction, then insert verified progress. Keep platform failures distinct from learner test failures and use correlation IDs in structured controller logs.
6. Import old local job history only as unverified history or rerun it through the evaluator. Do not promote browser-local solved flags to verified database progress.
7. Add RLS integration checks, storage policies and chosen-table realtime subscriptions before wiring the optional client into the active workspace.

## Verification status and commands

The Docker daemon was unavailable during implementation, so the authoring pass did not start the local services, execute a database reset, or run live RLS tests. SQL syntax/configuration checks and TypeScript checks are reported separately by the implementation handoff. The rollback-only SQL test file at supabase/tests/database/platform_rls.test.sql covers ownership, immutable records and progress evidence once local PostgreSQL is available:

~~~powershell
npm exec supabase -- db lint --local
npm exec supabase -- test db
~~~

Run those checks after the local stack starts. They are the remaining live database gate, including Supabase-specific roles and Auth behavior.

## Official references

- [Local CLI setup](https://supabase.com/docs/guides/local-development/cli/getting-started)
- [CLI configuration](https://supabase.com/docs/guides/local-development/cli/config)
- [Row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [JavaScript client initialization](https://supabase.com/docs/reference/javascript/initializing)
