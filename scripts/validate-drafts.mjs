import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import katex from 'katex';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = ['blueprint.md', 'statement.md', 'theory.md', 'examples.md', 'hints.md', 'review.md'];
function files(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? files(file) : [file];
  });
}
const paperIds = new Set(files(path.join(root, 'research/papers')).filter(file => file.endsWith('.md')).map(file => path.basename(file, '.md')));
const folders = process.argv.slice(2).length ? process.argv.slice(2).map(folder => path.resolve(root, folder))
  : files(path.join(root, 'content/planned')).filter(file => path.basename(file) === 'blueprint.md').map(file => path.dirname(file));
const errors = [];
const ids = new Set();
let equations = 0;
for (const folder of folders) {
  const label = path.relative(root, folder);
  const fail = message => errors.push(`${label}: ${message}`);
  for (const name of required) if (!fs.existsSync(path.join(folder, name))) fail(`missing ${name}`);
  if (!fs.existsSync(path.join(folder, 'blueprint.md'))) continue;
  let data;
  try { data = matter(fs.readFileSync(path.join(folder, 'blueprint.md'), 'utf8')).data; }
  catch (error) { fail(`invalid blueprint YAML: ${error.message}`); continue; }
  if (data.schema_version !== 1) fail('schema_version must be 1');
  if (!['drafted', 'reviewed'].includes(data.status)) fail('draft status must be drafted or reviewed');
  if (!data.problem_id || ids.has(data.problem_id)) fail('missing or duplicate problem_id');
  ids.add(data.problem_id);
  if (!data.title || !/^\d+\.\d+\.\d+$/.test(String(data.content_version))) fail('title or semantic content version missing');
  if (!data.entrypoint || !data.physical_contract || !data.grading || !data.provenance) fail('entrypoint, physical contract, grading, or provenance missing');
  if (!Array.isArray(data.paper_ids)) fail('paper_ids must be an array');
  else for (const id of data.paper_ids) if (!paperIds.has(id)) fail(`unknown source paper ${id}`);
  if (!data.runtime?.python || !data.runtime?.limits || !data.runtime?.dependencies) fail('runtime version, resource limits, or dependencies missing');
  if (Object.values(data.runtime?.dependencies || {}).some(version => /[<>*~^]/.test(String(version)))) fail('dependency versions must be exact');
  if (!Array.isArray(data.provenance?.primary_urls) || !data.provenance.primary_urls.length) fail('primary source URLs missing');
  for (const name of required) {
    const file = path.join(folder, name);
    if (!fs.existsSync(file)) continue;
    const markdown = matter(fs.readFileSync(file, 'utf8')).content.replace(/```[\s\S]*?```/g, '');
    const display = [...markdown.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(match => match[1]);
    const inline = [...markdown.replace(/\$\$[\s\S]*?\$\$/g, '').matchAll(/(?<!\\)\$([^$\n]+?)(?<!\\)\$/g)].map(match => match[1]);
    for (const math of [...display, ...inline]) {
      try { katex.renderToString(math, { throwOnError: true, strict: 'error' }); equations++; }
      catch (error) { fail(`${name} has invalid LaTeX: ${error.message}`); }
    }
    if (name === 'theory.md' && !display.length) fail('theory needs essential display mathematics');
  }
  if (fs.existsSync(path.join(folder, 'meta.json'))) fail('draft must not carry published application metadata');
}
if (errors.length) { console.error(errors.join('\n')); process.exitCode = 1; }
else console.log(`Draft structure and LaTeX valid: ${folders.length} packages, ${equations} expressions. Independent source, example, and pedagogy review still required.`);
