import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { fileURLToPath } from 'node:url';

const defaultRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const requiredProblemFiles = [
  'blueprint.md',
  'problem.md',
  'theory.md',
  'hints.md',
  'examples.md',
  'solution.md',
  'starter.py',
  'reference.py',
  'cases.py',
];
const difficulties = new Set(['Easy', 'Medium', 'Hard', 'Research']);

function markdownFiles(directory) {
  if (!fs.existsSync(directory)) return [];
  const found = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) found.push(...markdownFiles(fullPath));
    else if (entry.isFile() && entry.name.endsWith('.md')) found.push(fullPath);
  }
  return found;
}

function isHttpUrl(value) {
  try {
    const parsed = new URL(String(value));
    return parsed.protocol === 'https:' || parsed.protocol === 'http:';
  } catch {
    return false;
  }
}

export function validateContent(root = defaultRoot) {
  const repoRoot = path.resolve(root);
  const problemRoot = path.join(repoRoot, 'content', 'problems');
  const paperRoot = path.join(repoRoot, 'research', 'papers');
  const errors = [];
  const problemMetas = [];
  const papers = new Map();

  if (!fs.existsSync(problemRoot)) errors.push('Missing content/problems directory.');
  if (!fs.existsSync(paperRoot)) errors.push('Missing research/papers directory.');

  for (const file of markdownFiles(paperRoot)) {
    const relative = path.relative(repoRoot, file);
    try {
      const { data } = matter(fs.readFileSync(file, 'utf8'));
      const id = String(data.paper_id || '');
      if (!id) {
        errors.push(relative + ': missing paper_id in front matter.');
        continue;
      }
      if (!data.title || !Number.isInteger(Number(data.year)) || !isHttpUrl(data.primary_url)) {
        errors.push(relative + ': paper card needs a title, numeric year, and HTTP(S) primary_url.');
      }
      if (papers.has(id)) errors.push(relative + ': duplicate paper_id ' + id + '.');
      papers.set(id, relative);
    } catch (error) {
      errors.push(relative + ': could not parse Markdown front matter (' + error.message + ').');
    }
  }

  if (fs.existsSync(problemRoot)) {
    for (const entry of fs.readdirSync(problemRoot, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const directory = path.join(problemRoot, entry.name);
      const metaPath = path.join(directory, 'meta.json');
      if (!fs.existsSync(metaPath)) {
        errors.push('content/problems/' + entry.name + ': missing meta.json.');
        continue;
      }

      for (const name of requiredProblemFiles) {
        const file = path.join(directory, name);
        if (!fs.existsSync(file)) {
          errors.push('content/problems/' + entry.name + ': missing ' + name + '.');
        } else if (!fs.readFileSync(file, 'utf8').trim()) {
          errors.push('content/problems/' + entry.name + ': ' + name + ' is empty.');
        }
      }

      let meta;
      try {
        meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
      } catch (error) {
        errors.push('content/problems/' + entry.name + '/meta.json: invalid JSON (' + error.message + ').');
        continue;
      }

      if (!meta || typeof meta !== 'object' || Array.isArray(meta)) {
        errors.push('content/problems/' + entry.name + '/meta.json: expected an object.');
        continue;
      }
      if (meta.slug !== entry.name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(String(meta.slug || ''))) {
        errors.push('content/problems/' + entry.name + ': slug must match its lowercase directory name.');
      }
      if (!meta.title || typeof meta.title !== 'string') errors.push(entry.name + ': missing title.');
      if (!/^\d+\.\d+\.\d+$/.test(String(meta.version || ''))) errors.push(entry.name + ': version must use semantic x.y.z form.');
      if (!Number.isInteger(meta.number) || meta.number < 1) errors.push(entry.name + ': number must be a positive integer.');
      if (!difficulties.has(meta.difficulty)) errors.push(entry.name + ': unsupported difficulty.');
      if (!meta.domain || !meta.framework || !meta.entrypoint || !meta.summary) {
        errors.push(entry.name + ': domain, framework, entrypoint, and summary are required.');
      }
      if (!Array.isArray(meta.topics) || meta.topics.length === 0) errors.push(entry.name + ': topics must be a non-empty array.');
      if (!Array.isArray(meta.prerequisites)) errors.push(entry.name + ': prerequisites must be an array.');
      if (!Array.isArray(meta.paperIds)) errors.push(entry.name + ': paperIds must be an array.');
      problemMetas.push({ slug: entry.name, meta });
    }
  }

  const numbers = new Set();
  const slugs = new Set(problemMetas.map(problem => problem.slug));
  for (const { slug, meta } of problemMetas) {
    if (Number.isInteger(meta.number)) {
      if (numbers.has(meta.number)) errors.push(slug + ': duplicate problem number ' + meta.number + '.');
      numbers.add(meta.number);
    }
    for (const prerequisite of Array.isArray(meta.prerequisites) ? meta.prerequisites : []) {
      if (!slugs.has(prerequisite)) errors.push(slug + ': unknown prerequisite ' + prerequisite + '.');
    }
    for (const paperId of Array.isArray(meta.paperIds) ? meta.paperIds : []) {
      if (!papers.has(paperId)) errors.push(slug + ': unknown paperId ' + paperId + '.');
    }
  }

  return { errors, problemCount: problemMetas.length, paperCount: papers.size };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = validateContent(process.argv[2] || defaultRoot);
  if (result.errors.length) {
    console.error('Content validation failed with ' + result.errors.length + ' issue(s):');
    for (const error of result.errors) console.error('- ' + error);
    process.exitCode = 1;
  } else {
    console.log('Content valid: ' + result.problemCount + ' problems and ' + result.paperCount + ' paper cards.');
  }
}
