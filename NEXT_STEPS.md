# Current release work

The original 190 named curriculum problems are implemented. The current checkpoint has 321 runnable packages: the original 193, four bounded capstones and 124 reviewed paper additions. Three paper integrations implement a tiny PPO controller, a calibrated SmoothQuant layer and a small NeRF field training loop. The reviewed expansion is indexed in CURRICULUM.md section 7; remaining paper ideas are tracked explicitly in research/IMPLEMENTATION_BACKLOG.md.

## Implemented in this release pass

- Account-scoped draft, note and bookmark sync with Supabase Auth/RLS, revision conflicts, guest isolation and quota recovery. All four migrations and 321 catalog-only versions are applied to the authorized hosted project.
- Service-only atomic evaluation history and verified progress recording; browser claims cannot create scores. The worker reports through the authenticated web control plane and has no general database key.
- Four runnable capstones and PPO/SmoothQuant/NeRF paper integrations, each with original theory, evaluation/failure cases and a reproducibility template. Projects and Tracks distinguish runnable integrations from proposals.
- A prepared authenticated Linux backend topology and experimental data-only grader. The existing local native runner remains available.

## Still in progress

- Additional paper-component batches: research-curator owns RL/humanoid and registry/source review; perception agent owns geometry/planning; MLOps agent owns data/deployment/simulation. The backlog contains hundreds of proposed titles; reviewed reuse and publication reduce it explicitly.
- Further paper-specific integrations. Three executable paper projects (PPO, SmoothQuant and NeRF) are available; the other paper integration proposals are not automatically complete because atomic problems exist.
- A production grading boundary compatible with native mutation/aliasing/autograd contracts. The experimental value-only transport cannot qualify the existing catalog by weakening those guarantees. See deploy/README.md.
- Live signed-in account save/reload confirmation. Schema/catalog provisioning and anonymous access boundaries are verified; no real test account has been created automatically.
- Selecting the Linux backend host and qualifying its actual image, containment and cleanup. The user requested deployment preparation and will choose hosting.

## Verification and publishing

The four capstones passed actual Run/Submit, starter and mechanism-mutant checks and independent review. The first12RL additions passed their focused isolated checks. Account sync passed browser conflict/account-switch tests, unit/auth tests and49 PostgreSQL assertions in an isolated PGlite database. Hosted migration history and all321 published identities match the local plan. Anonymous catalog access succeeds; draft access and trusted evaluation writes are denied. The 321-problem content validator, seven-project validator and refreshed paper-track/link validators pass. Each newly published batch passed focused sandbox Run/Submit and starter/mechanism-mutant checks plus independent review. The prior web checkpoint d045b0e passed its production build and Vercel deployment; this content-only follow-up is verified by its subsequent Vercel build. Representative new Theory pages passed desktop/narrow-screen checks with math, trace tables and the adjacent editor.

GitHub issue/PR posting has no authenticated interface in this workspace. Keep concrete issue drafts without retrying the previously rejected credential-access method. Ordinary Git commit/push remains available. A local fix, pushed branch and merged PR are different states; do not conflate them.
