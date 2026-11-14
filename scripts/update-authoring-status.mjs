import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = file => fs.readFileSync(file, 'utf8');
const normalize = title => title.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
const slash = value => value.split(path.sep).join('/');
const paperSources = new Set();
function countPapers(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) countPapers(file);
    else if (entry.name.endsWith('.md')) {
      const { data } = matter(read(file));
      if (data.primary_url) paperSources.add(String(data.primary_url).trim().replace(/\/$/, ''));
    }
  }
}
countPapers(path.join(root, 'research/papers'));
const published = new Map();
for (const name of fs.readdirSync(path.join(root, 'content/problems'))) {
  const folder = `content/problems/${name}`;
  if (!fs.existsSync(path.join(root, folder, 'meta.json'))) continue;
  const meta = JSON.parse(read(path.join(root, folder, 'meta.json')));
  published.set(normalize(meta.title), { folder, slug: meta.slug });
}
const equivalentTitles = {
  'Decode YOLO Grid Predictions into Image Boxes': 'Decode YOLO Grid Predictions',
  'Compute Symmetric Contrastive Loss': 'Compute Symmetric CLIP Contrastive Loss',
  'Quantize and Dequantize Continuous Robot Actions': 'Quantize and Decode Robot Actions',
};
const publishedCount = published.size;
for (const [curriculumTitle, publishedTitle] of Object.entries(equivalentTitles)) {
  const problem = published.get(normalize(publishedTitle));
  if (problem) published.set(normalize(curriculumTitle), problem);
}
const drafts = new Map();
function scan(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) scan(file);
    else if (['metadata.md', 'blueprint.md'].includes(entry.name)) {
      const { data } = matter(read(file));
      if (!data.title) continue;
      const folder = path.dirname(file);
      const complete = ['blueprint.md', 'statement.md', 'theory.md', 'hints.md', 'examples.md', 'review.md'].every(name => fs.existsSync(path.join(folder, name)));
      const key = normalize(String(data.title));
      if (!drafts.has(key) || entry.name === 'blueprint.md') drafts.set(key, { folder: slash(path.relative(root, folder)), complete, reviewed: data.status === 'reviewed' && Array.isArray(data.reviewers) && data.reviewers.length > 0 });
    }
  }
}
scan(path.join(root, 'content/planned'));
const sections = new Map();
let section, group;
for (const line of read(path.join(root, 'CURRICULUM.md')).split(/\r?\n/)) {
  if (line.startsWith('## ')) section = line.slice(3);
  if (line.startsWith('### ')) group = line.slice(4);
  const match = line.match(/^- `\[(foundation|paper|systems)\]` (.+)$/);
  if (!match) continue;
  const title = match[2], key = normalize(title), runnable = published.get(key), draft = drafts.get(key);
  const status = runnable ? 'Runnable' : draft?.complete && draft.reviewed ? 'Reviewed draft; evaluator pending' : draft?.complete ? 'Draft package; review pending' : draft ? 'Existing plan; contract review pending' : 'Queued';
  const folder = runnable?.folder || draft?.folder;
  const item = { title, group, status, folder };
  if (!sections.has(section)) sections.set(section, []);
  sections.get(section).push(item);
}
const all = [...sections.values()].flat();
const lines = [
  '# Curriculum authoring status', '',
  'Generated from `CURRICULUM.md`, published metadata, and existing draft folders. Refresh with `node scripts/update-authoring-status.mjs`. A complete file package is **not** an independent review or a published evaluator.', '',
  `Scope: **${all.length} named curriculum problems**, plus the four integration capstone sequences. The corpus has ${paperSources.size} distinct papers; not every collected paper has an approved problem in this roadmap. Additional ideas attached to paper flow nodes remain unreviewed until promoted through a blueprint.`, '',
  `Coverage: ${all.filter(item => item.status === 'Runnable').length} named entries map directly to published tasks; ${all.filter(item => item.status.startsWith('Reviewed')).length} have independently reviewed drafts; ${all.filter(item => item.status.startsWith('Draft')).length} have draft packages awaiting review; ${all.filter(item => item.status.startsWith('Existing')).length} have earlier plans; ${all.filter(item => item.status === 'Queued').length} remain queued. The application has ${publishedCount} published problems; some are supporting components rather than identical named roadmap entries.`, '',
  '## Work and review lanes', '',
  '| Lane | Author | Independent reviewer |', '|---|---|---|',
  '| Foundations and integration | Main agent | Robotics/perception author |',
  '| Vision, VLM, 3D perception | Robotics/perception author | VLA research curator |',
  '| VLA and embodied learning | VLA research curator | MLOps/evaluator author |',
  '| MLOps, deployment, sim-to-real | MLOps/evaluator author | Robotics/perception author |', '',
  'Authors start with six concrete components per lane. Reviewers check source fidelity, numerical examples, physical contracts, edge cases, and theory clarity. Confirmed findings receive reproducible issue drafts; fixes return to the independent reviewer before integration. The main agent reviews the resulting changes and merges ready PRs when publishing is available.', '',
  'GitHub publishing currently lacks an available authenticated interface; an earlier credential-access attempt was rejected by automatic approval review. Local issue drafts and fix branches are retained without retrying that method.', '',
  'Drafts live under `content/planned/` with `blueprint.md`, `statement.md`, `theory.md`, `hints.md`, `examples.md`, and `review.md`. They must not receive published `meta.json` or runnable links until their reference solutions, public/hidden tests, and isolated evaluators are verified.', '',
];
for (const [name, entries] of sections) {
  lines.push(`## ${name}`, '', '| Problem | Group | State |', '|---|---|---|');
  for (const item of entries) {
    const title = item.title.replaceAll('|', '\\|');
    const label = item.folder ? `[${title}](${item.folder.replace(/^content\//, '')}/)` : title;
    lines.push(`| ${label} | ${item.group.split(' ')[0]} | ${item.status} |`);
  }
  lines.push('');
}
fs.writeFileSync(path.join(root, 'content/AUTHORING_STATUS.md'), lines.join('\n'));
console.log(`Updated authoring status for ${all.length} named curriculum problems.`);
