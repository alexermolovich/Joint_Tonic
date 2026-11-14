# Release implementation plan

Requested 2026-11-14. The user authorized the remaining platform and content work, commits and web publishing. The evaluator/simulator deployment is to be prepared; the user will choose its hosting provider. Do not claim that preparation deploys those services.

## Work allocation

| Owner | Deliverable | Evidence required |
|---|---|---|
| Account agent | Supabase drafts, notes, bookmarks, verified progress and submission history; isolated account caches and conflict handling | Ownership/RLS tests, account-switch and stale-save tests, migration checks |
| Capstone agent | Four runnable cross-paper projects: grounded perception, VLA release, edge deployment, sim-to-real reliability | Explicit bounded contracts, original theory, public/hidden checks, failure analysis and reproducibility notes |
| Research curator | Review and deduplicate remaining paper ideas, implement components in topic batches, update paper graphs | Primary-source fidelity, reviewed blueprints, isolated reference/starter/mutant checks |
| Main agent | Backend deployment preparation, authenticated integration, focused UI review, final integration and Git publishing | Fail-closed configuration, bounded execution, reproducible setup, regression checks and verified deployment state |

All four available slots are occupied. Agents preserve each other's uncommitted files and send contract changes before editing shared interfaces.

## Content boundary

The completed baseline contains 190 named curriculum entries / 193 runnable packages. The expanded paper inventory initially contains 457 proposed associations, 450 unique titles and seven exact-title candidates already implemented. The remaining 443 titles need semantic deduplication and contract review; this is not a claim that 443 new problems are already published. Track each promotion in [the implementation backlog](../research/IMPLEMENTATION_BACKLOG.md).

Do not replace pending paper stages with generic links just to report completion. A bounded synthetic project must state its deviations from full-paper training and benchmark results.

## Integration order

1. Preserve the completed curriculum baseline and allocate nonoverlapping files/IDs.
2. Add account synchronization and database contracts; verify ownership before enabling hosted writes.
3. Prepare separate Linux evaluator and simulator services, authentication and deployment configuration. Learner code never executes inside Vercel or Supabase functions.
4. Integrate capstones and reviewed paper-component batches; update generated indexes only after contracts and evaluators pass.
5. Run focused checks, production build and representative desktop/mobile browser checks.
6. Commit and push reviewed changes; verify the Vercel result. Report any pending migration, hosting or grading-security requirement explicitly.

## External inputs

- Backend hosting: intentionally pending the user's choice; prepare artifacts and commands only.
- Supabase: the user agreed to configure CLI authentication or `SUPABASE_DB_URL`. Verify availability without printing credentials; a text confirmation is not a working connection.
- Public hostile-code grading: the existing local runner shares learner and test interpreters. Do not expose it as a trustworthy public evaluator without the stronger trust boundary described in the worker documentation.
