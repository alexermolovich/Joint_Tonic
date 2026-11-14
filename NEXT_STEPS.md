# Current release work

The original 190 named curriculum problems are implemented. The current checkpoint has 209 runnable packages: the original193, four bounded capstones and12RL additions including a tiny PPO controller integration. The reviewed expansion is indexed in CURRICULUM.md section7; pending paper ideas remain explicitly tracked in research/IMPLEMENTATION_BACKLOG.md.

## Implemented in this release pass

- Account-scoped draft, note and bookmark sync with Supabase Auth/RLS, revision conflicts, guest isolation and quota recovery. Database migrations and published catalog versions are prerequisites for hosted use.
- Service-only atomic evaluation history and verified progress recording; browser claims cannot create scores. The worker reports through the authenticated web control plane and has no general database key.
- Four runnable capstones and a PPO paper integration, each with original theory, evaluation/failure cases and a reproducibility template. Projects and Tracks distinguish runnable integrations from proposals.
- A prepared authenticated Linux backend topology and experimental data-only grader. The existing local native runner remains available.

## Still in progress

- Additional paper-component batches: research-curator owns RL/humanoid and registry/source review; perception agent owns geometry/planning; MLOps agent owns data/deployment/simulation. The backlog contains hundreds of proposed titles; reviewed reuse and publication reduce it explicitly.
- Further paper-specific integrations. One executable PPO paper project is available; the other paper integration proposals are not automatically complete because atomic problems exist.
- A production grading boundary compatible with native mutation/aliasing/autograd contracts. The experimental value-only transport cannot qualify the existing catalog by weakening those guarantees. See deploy/README.md.
- Applying hosted Supabase migrations/catalog: CLI authentication or a database connection is still required. A publishable key alone cannot apply schema changes.
- Selecting the Linux backend host and qualifying its actual image, containment and cleanup. The user requested deployment preparation and will choose hosting.

## Verification and publishing

The four capstones passed actual Run/Submit, starter and mechanism-mutant checks and independent review. The first12RL additions passed their focused isolated checks. Account sync passed browser conflict/account-switch tests, unit/auth tests and44 PostgreSQL assertions in an isolated PGlite database. Hosted PostgREST/migration behavior remains unverified until connected. The209-problem content validator, five-project validator, paper-track/link validators and production build pass at this checkpoint.

GitHub issue/PR posting has no authenticated interface in this workspace. Keep concrete issue drafts without retrying the previously rejected credential-access method. Ordinary Git commit/push remains available. A local fix, pushed branch and merged PR are different states; do not conflate them.
