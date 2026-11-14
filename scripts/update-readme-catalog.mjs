import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const start = '<!-- GENERATED CATALOG START -->';
const end = '<!-- GENERATED CATALOG END -->';
const escape = value => String(value).replace(/\|/g, '&#124;').replace(/[\r\n]+/g, ' ').replace(/\[/g, '&#91;').replace(/\]/g, '&#93;');
const localTargets = new Set();
function link(label, target) {
  if (!/^https?:\/\//.test(target)) {
    if (!fs.existsSync(path.join(root, target))) throw new Error(`Missing link target: ${target}`);
    localTargets.add(target);
  }
  return `[${escape(label)}](<${target}>)`;
}
function markdownFiles(directory) {
  return fs.readdirSync(path.join(root, directory), { withFileTypes: true }).flatMap(entry => {
    const file = `${directory}/${entry.name}`;
    return entry.isDirectory() ? markdownFiles(file) : entry.name.endsWith('.md') ? [file] : [];
  }).sort();
}
const problems = fs.readdirSync(path.join(root, 'content/problems')).flatMap(slug => {
  const folder = `content/problems/${slug}`;
  if (!fs.existsSync(path.join(root, folder, 'meta.json'))) return [];
  const meta = JSON.parse(read(`${folder}/meta.json`));
  if (meta.slug !== slug) throw new Error(`Problem slug does not match folder: ${slug}`);
  return [{ ...meta, folder }];
}).sort((a, b) => a.number - b.number || a.slug.localeCompare(b.slug));
const problemBySlug = new Map(problems.map(problem => [problem.slug, problem]));
const papers = markdownFiles('research/papers').map(file => {
  const { data } = matter(read(file));
  if (!data.paper_id || !data.title || !data.primary_url || !data.pdf_url) throw new Error(`Incomplete paper metadata: ${file}`);
  return { ...data, file, collection: file.split('/')[2] };
});
const paperById = new Map(papers.map(paper => [paper.paper_id, paper]));
if (paperById.size !== papers.length) throw new Error('Duplicate paper IDs');
const related = new Map(papers.map(paper => [paper.paper_id, new Set()]));
for (const problem of problems) {
  for (const id of problem.paperIds ?? []) {
    if (!paperById.has(id)) throw new Error(`Unknown paper ${id} in ${problem.slug}`);
    related.get(id).add(problem.slug);
  }
}
for (const paper of papers) {
  for (const node of paper.execution_flow?.nodes ?? []) {
    for (const slug of node.problem_slugs ?? []) {
      if (!problemBySlug.has(slug)) throw new Error(`Unknown problem ${slug} in ${paper.paper_id}`);
      related.get(paper.paper_id).add(slug);
    }
  }
}
const domains = [...new Set(problems.map(problem => problem.domain))].sort();
const collections = [...new Set(papers.map(paper => paper.collection))].sort();
const distinctPapers = new Set(papers.map(paper => String(paper.primary_url).trim().replace(/\/$/, ''))).size;
const lines = [start, '## Complete problem and paper catalog', '',
  `**${problems.length} runnable problems · ${papers.length} paper cards · ${distinctPapers} distinct primary papers.**`, '',
  'Problem metadata records the version, difficulty, runtime and provenance. Each problem links directly to its statement and mathematical theory. Paper cards contain YAML metadata, original explanations, math and execution flows; their source links lead to the original publications.', '',
  'The same primary paper can have more than one topic card. Related exercises below combine explicit problem provenance with paper execution-flow associations; an association does not claim a complete paper reproduction. Planned components remain in the [implementation backlog](research/IMPLEMENTATION_BACKLOG.md). PDFs stay in the local reference library; the links below point to publicly available source PDFs.', '',
  'Regenerate this catalog after adding or changing content:', '', '```sh', 'node scripts/update-readme-catalog.mjs', '```', '',
  'Check that it is current without changing files: `node scripts/update-readme-catalog.mjs --check`.', '',
  '### Browse problems by domain', ''];
for (const [index, domain] of domains.entries()) {
  lines.push(`- [${escape(domain)}](#catalog-problems-${index + 1}) (${problems.filter(problem => problem.domain === domain).length})`);
}
lines.push('', '### Browse papers by topic', '');
for (const collection of collections) {
  lines.push(`- [${collection}](#catalog-papers-${collection}) (${papers.filter(paper => paper.collection === collection).length} cards)`);
}
for (const [index, domain] of domains.entries()) {
  lines.push('', `<a id="catalog-problems-${index + 1}"></a>`, '', `### ${escape(domain)} problems`, '',
    '| # | Problem | Difficulty | Metadata | Theory | Paper provenance |',
    '| --- | --- | --- | --- | --- | --- |');
  for (const problem of problems.filter(problem => problem.domain === domain)) {
    const sources = (problem.paperIds ?? []).map(id => link(id, paperById.get(id).file)).join('<br>') || '—';
    lines.push(`| ${problem.number} | ${link(problem.title, `${problem.folder}/problem.md`)} | ${escape(problem.difficulty)} | ${link(`v${problem.version}`, `${problem.folder}/meta.json`)} | ${link('Theory', `${problem.folder}/theory.md`)} | ${sources} |`);
  }
}
for (const collection of collections) {
  lines.push('', `<a id="catalog-papers-${collection}"></a>`, '', `### ${collection} papers`, '',
    '| Paper | Metadata, explanation & math | Original sources | Related runnable problems |',
    '| --- | --- | --- | --- |');
  for (const paper of papers.filter(paper => paper.collection === collection).sort((a, b) => a.year - b.year || a.title.localeCompare(b.title))) {
    const exercises = [...related.get(paper.paper_id)].map(slug => problemBySlug.get(slug)).sort((a, b) => a.number - b.number);
    const links = exercises.map(problem => link(problem.title, `${problem.folder}/problem.md`)).join('<br>') || 'No linked runnable component yet';
    lines.push(`| ${escape(paper.title)} (${paper.year}) | ${link(paper.paper_id, paper.file)} | ${link('Publication', paper.primary_url)} · ${link('PDF', paper.pdf_url)} | ${links} |`);
  }
}
lines.push('', end);
const current = read('README.md').replace(/\r\n/g, '\n');
const startIndex = current.indexOf(start);
const endIndex = current.indexOf(end);
if ((startIndex === -1) !== (endIndex === -1) || (startIndex !== -1 && endIndex < startIndex)) throw new Error('Malformed README catalog markers');
const generated = lines.join('\n');
const next = startIndex === -1
  ? `${current.trimEnd()}\n\n${generated}\n`
  : current.slice(0, startIndex) + generated + current.slice(endIndex + end.length);
if (process.argv.includes('--check')) {
  if (current !== next) throw new Error('README catalog is stale. Run node scripts/update-readme-catalog.mjs');
} else {
  fs.writeFileSync(path.join(root, 'README.md'), next);
}
console.log(`${process.argv.includes('--check') ? 'Checked' : 'Generated'} README catalog: ${problems.length} problems, ${papers.length} paper cards, ${distinctPapers} distinct papers; ${localTargets.size} local link targets verified.`);
