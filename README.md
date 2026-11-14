# Joint Tonic

Implement robotics and physical-AI components through coding problems, mathematical explanations and research-paper tracks.

- **274 runnable problems** at the current release checkpoint, including all 190 original curriculum entries, four capstones, plus PPO and SmoothQuant integrations. Further paper batches are tracked in the [implementation backlog](research/IMPLEMENTATION_BACKLOG.md).
- **156 paper tracks**, backed by 157 original Markdown cards and locally retained reference PDFs.
- Python/NumPy/PyTorch evaluation in a separate local worker; an optional live MuJoCo FR3 workspace.

## Local preview

In the configured development workspace:

```text
npm ci
npm run dev
```

Open [Problems](http://localhost:3000/problems), [Tracks](http://localhost:3000/tracks), or [Projects](http://localhost:3000/projects).

The web app uses Node.js 24. Evaluation requires Linux/WSL, bubblewrap and the pinned Python 3.12.3 environment with NumPy 2.2.4 and PyTorch 2.6.0 CPU. The current Windows launcher uses `/home/alex/.venvs/joint-tonic/bin/python`; configure an equivalent environment using [the worker instructions](apps/worker/README.md). [MuJoCo setup](docs/mujoco-fr3.md) describes the simulator and pinned assets. The web-only command is `npm run web`.

Hosted credentials are optional for local browsing and practice. [Supabase Auth setup](docs/supabase-auth.md) documents the account and synchronization flows. Applied migrations and published catalog versions are required for account storage. The [Vercel web deployment guide](docs/vercel-web.md) and [separate backend preparation](deploy/README.md) keep evaluation and simulation outside serverless functions.

## Content and architecture

- [Curriculum topic tree](CURRICULUM.md) and [runnable package index](content/AUTHORING_STATUS.md).
- [Completion and verification](content/CURRICULUM_COMPLETION.md).
- [Paper tracks](content/PAPER_TRACKS.md), [paper-to-code flow map](research/FLOW_PROBLEM_MAP.md), and [research library](research/README.md).
- [Product specification](SPEC.md), [contributor instructions](AGENTS.md), and [remaining platform work](NEXT_STEPS.md).

PDFs are local research references, excluded from Git and web deployment. Cards link to canonical sources and record access/provenance status. Four bounded capstones are available under Projects. They use synthetic fixtures and do not claim full-paper training reproduction.
