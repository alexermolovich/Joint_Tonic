# Vercel web deployment

The Vercel project uses the **repository root** (leave Root Directory empty or `.`), where `package.json` and `package-lock.json` live. Do not set the root to `apps/web` for this configuration.

Checked-in `vercel.json` sets the Next.js framework, `npm ci`, the production build command, and output directory **`apps/web/.next`**. `npm run build` invokes Next with `apps/web`, so `.next` at the repository root is not its output. This fixes the missing-output-directory error reported for commit 8cdf319.

The build prepares local Monaco assets even on a clean checkout. The final Vercel preparation step copies the app's public files into generated root `public/`, where the repository-root Vercel builder collects static assets. Both generated locations are ignored by Git. The Next configuration traces required Markdown/metadata/reference files outside `apps/web` for dynamic server routes, while excluding local runtime data, research PDFs and hidden cases.

## Project setup

- Framework: Next.js.
- Root Directory: repository root.
- Build command/output: use the checked-in `vercel.json` settings, not an override targeting `.next` at root.
- Environment: configure `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` for the desired Vercel environments. Local `.env.local` is deliberately not committed or uploaded. Never add the Supabase secret key to client environment variables.
- After the deployed domain is known, allow its `/account` and `/auth/reset-password` URLs in Supabase Auth; localhost redirects alone do not configure hosted login callbacks.

The hosted web preview does **not** deploy the Python evaluator or MuJoCo service. Existing local UUID ownership and loopback simulator/evaluator services must not be exposed as a public backend. Hosted Run/Submit and Simulation remain unavailable until a separately authorized authenticated, isolated backend deployment is implemented. Browsing the curriculum and using the editor do not require these services.

## Verify

Run `npm run build`, then `node scripts/prepare-vercel-public.mjs`. Check `apps/web/.next/routes-manifest.json`, the traced lesson files in dynamic page `.nft.json` manifests, and generated `public/monaco/vs/loader.js`. A local Next build verifies the application artifact; only Vercel's subsequent deployment can verify its hosted packaging and project environment settings.

References: [Vercel configuration](https://vercel.com/docs/project-configuration/vercel-json), [Next file tracing](https://nextjs.org/docs/app/api-reference/config/next-config-js/output).
