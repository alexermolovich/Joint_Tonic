# Separate Linux backend deployment

The user is choosing a hosting provider. These are preparation artifacts, not a deployed backend. The web stays on Vercel; Auth/data stay on Supabase. Use a dedicated Linux host for code execution and MuJoCo. No learner code runs in Vercel/Supabase functions.

## Current readiness and limits

- The authenticated Next proxy validates the Supabase session before sending the server-only backend credential and account ID. It preserves signed-out loopback development.
- `production_server.py` accepts only the authenticated proxy, binds loopback, and requires gVisor, a digest-pinned runtime image, an authenticated control-plane callback, and a matching qualification manifest. It never falls back to the development shared-interpreter harness. The worker has no general database credential.
- The trusted grader retains authored cases in its own process and exchanges bounded data-only function inputs/outputs with a separate learner process. A learner-provided verdict is not an authoritative result. Pickle and object deserialization are not supported.
- **The initial protocol supports Python/NumPy value-returning functions only.** It preserves numeric dtypes and bounded array strides, including negative and broadcast strides. Arrays are copied across the boundary; shared-object identity, in-place effects and PyTorch autograd need additional protocol work and qualification. Passing the v1 checks does not establish those contracts. Do not enable exercises that require unsupported semantics.
- Qualification requires an explicit, reviewed `execution_contract` declaring this value-only protocol. Existing native-function exercises do not have this declaration and remain blocked from hosted execution. In particular, the adapter's copies would hide input mutation from a native immutability test. A separate reviewed semantic version or a stronger native-function grading boundary is required; do not silently remove that guarantee to enable deployment.
- The initial boundary checks passed on Linux bubblewrap. Docker/gVisor image builds, aggregate cgroup limits and the actual TLS deployment have **not** been exercised here: the workspace has no running Docker daemon and no selected host. The production entrypoint fails closed until a gVisor qualification manifest exists.

## Host requirements

Use Linux with Docker, cgroup memory/CPU/PID accounting and gVisor's `runsc` Docker runtime. The trusted worker launches at most two learner jobs concurrently; each has 4 GiB memory, one CPU, 64 processes, no network, a read-only filesystem, dropped capabilities and an 18-second wall deadline. Provision memory for both jobs, the trusted grader and the renderer. Keep this host separate from unrelated services and secrets: the trusted worker's Docker access is privileged host access.

Install gVisor using its [official installation instructions](https://gvisor.dev/docs/user_guide/install/) and [Docker integration](https://gvisor.dev/docs/user_guide/quick_start/docker/). Docker's default seccomp policy remains active in addition to gVisor and capability restrictions. Validate containment on the chosen kernel/runtime before exposing traffic.

## Prepare artifacts

1. Check out the reviewed Git commit under `/opt/joint-tonic`. Create a `joint-tonic` system user, `.local/runtime-work` writable by that user, and a Python 3.12.3 virtual environment. Install the pinned NumPy/PyTorch runtime required by authored tests and `apps/simulator/requirements.txt` for the renderer. Use `apps/simulator/setup_assets.py` to acquire and verify the pinned FR3 assets before applying the read-only service protections.
2. Build the **learner-only** image with a minimal build context:

   ```sh
   docker build -f deploy/runtime.Dockerfile -t YOUR_REGISTRY/joint-tonic-runtime:reviewed deploy
   docker push YOUR_REGISTRY/joint-tonic-runtime:reviewed
   docker inspect --format '{{json .RepoDigests}}' YOUR_REGISTRY/joint-tonic-runtime:reviewed
   ```

   Record the actual returned `name@sha256:...` as `JOINT_TONIC_RUNTIME_IMAGE`. Never substitute a source hash for an image digest. The image contains no PDFs, cases, reference solutions or credentials.
3. Generate distinct random `WORKER_SERVICE_TOKEN` and `SIMULATOR_SERVICE_TOKEN` values with at least 32 characters. Store them in the root-owned `/etc/joint-tonic/*.env` files based on the examples. Give only the trusted service group read access. Configure the same tokens as **server-only** Vercel variables. Configure `SUPABASE_SECRET_KEY` only in the trusted Vercel control plane, never on the worker or in the learner image/browser. `CONTROL_PLANE_URL` identifies the HTTPS web origin; the authenticated `/api/evaluations` callback validates and records immutable results through the service-only database RPC.
4. Apply the reviewed Supabase migrations and publish catalog versions with the actual runtime image digest using the repository catalog-sync command. Drafts/notes can sync only for catalog versions that exist in the database. Do not manufacture published metadata to bypass this step.
5. After implementing and independently reviewing compatible content revisions, qualify those explicit slugs on the actual gVisor image:

   ```sh
   .venv/bin/python apps/worker/qualify_runtime.py --output .local/qualification.json REVIEWED_VALUE_ONLY_SLUG
   ```

   The manifest pins source and grader hashes. References must pass Run/Submit, and incomplete starters and forged result objects must fail. Review protocol compatibility as well as test results. Changes to cases, metadata, starter, reference or grader require requalification. Do not add PyTorch/autograd exercises to this initial NumPy image.

## Start and connect

Install the two systemd units, reviewed environment files and Caddy configuration. Set `WORKER_DOMAIN` and `SIMULATOR_DOMAIN` to hostnames with DNS pointed at the selected host. Expose only TLS and administrative access; ports 8765/8766 stay bound to loopback. Caddy terminates TLS and imposes request-body limits; backend authentication remains required.

Set Vercel's `WORKER_URL=https://WORKER_DOMAIN`, `SIMULATOR_URL=https://SIMULATOR_DOMAIN` and their corresponding server-only service tokens. Preserve the public Supabase URL/publishable-key settings. Configure the deployed account/reset-password redirects in Supabase Auth. Never put service tokens or database keys in `NEXT_PUBLIC_*` variables.

## Acceptance and rollback

- Verify missing/invalid session rejection, wrong-account job reads, request limits, queue saturation, CPU/wall/output termination, container removal and network/filesystem isolation.
- Test Docker-daemon failure during cleanup. Cleanup failures emit `sandbox.cleanup_failed`; an external host reaper must remove stale job containers and block admission when cleanup cannot be confirmed. Wall-clock containment during daemon failure is not established by the local protocol checks.
- Verify a real signed-in Run/Submit, durable server-recorded history, reload, and second-device progress. Anonymous browser-local solves are not uploaded as verified passes.
- Verify FR3 camera orbit and actual output-driven playback, with a malformed joint/camera request rejected. The renderer consumes only bounded numbers, never learner source.
- Review service logs by correlation ID; do not log code, access tokens or private notes.
- Roll back the web Git deployment and the worker Git commit/image/qualification manifest together. Preserve database history and immutable versions. Stop accepting work before switching the worker release; never mutate content in a running release directory.

Remaining production support and host verification must stay visible in the release status. Publishing the frontend alone does not complete this checklist.
