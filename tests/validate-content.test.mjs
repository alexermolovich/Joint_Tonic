import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { validateContent } from '../scripts/validate-content.mjs';

const requiredFiles = [
  'blueprint.md', 'problem.md', 'theory.md', 'hints.md', 'examples.md',
  'solution.md', 'starter.py', 'reference.py', 'cases.py',
];

function createFixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'joint-tonic-content-'));
  const problemDir = path.join(root, 'content', 'problems', 'test-problem');
  const paperDir = path.join(root, 'research', 'papers', 'robot-learning');
  fs.mkdirSync(problemDir, { recursive: true });
  fs.mkdirSync(paperDir, { recursive: true });
  const meta = {
    slug: 'test-problem',
    title: 'Test problem',
    version: '1.0.0',
    number: 1,
    difficulty: 'Easy',
    domain: 'Geometry',
    topics: ['frames'],
    framework: 'NumPy',
    entrypoint: 'transform_points',
    paperIds: ['2024-test-paper'],
    prerequisites: [],
    summary: 'A small fixture problem.',
  };
  fs.writeFileSync(path.join(problemDir, 'meta.json'), JSON.stringify(meta));
  for (const name of requiredFiles) fs.writeFileSync(path.join(problemDir, name), 'content\n');
  fs.writeFileSync(path.join(paperDir, '2024-test-paper.md'), [
    '---',
    'paper_id: 2024-test-paper',
    'title: Test paper',
    'year: 2024',
    'primary_url: https://example.org/paper',
    '---',
    '',
    'Agent summary.',
  ].join('\n'));
  return { root, problemDir, meta };
}

test('accepts a complete problem with a linked paper card', t => {
  const fixture = createFixture();
  t.after(() => fs.rmSync(fixture.root, { recursive: true, force: true }));
  assert.deepEqual(validateContent(fixture.root), { errors: [], problemCount: 1, paperCount: 1 });
});

test('reports missing required problem files', t => {
  const fixture = createFixture();
  t.after(() => fs.rmSync(fixture.root, { recursive: true, force: true }));
  fs.rmSync(path.join(fixture.problemDir, 'theory.md'));
  const result = validateContent(fixture.root);
  assert.ok(result.errors.some(error => error.includes('missing theory.md')));
});

test('reports duplicate numbers and broken paper and prerequisite links', t => {
  const fixture = createFixture();
  t.after(() => fs.rmSync(fixture.root, { recursive: true, force: true }));
  fixture.meta.prerequisites = ['missing-prerequisite'];
  fixture.meta.paperIds = ['missing-paper'];
  fs.writeFileSync(path.join(fixture.problemDir, 'meta.json'), JSON.stringify(fixture.meta));
  const secondDir = path.join(fixture.root, 'content', 'problems', 'second-problem');
  fs.mkdirSync(secondDir, { recursive: true });
  fs.writeFileSync(path.join(secondDir, 'meta.json'), JSON.stringify({
    ...fixture.meta,
    slug: 'second-problem',
    prerequisites: [],
  }));
  for (const name of requiredFiles) fs.writeFileSync(path.join(secondDir, name), 'content\n');
  const errors = validateContent(fixture.root).errors.join('\n');
  assert.match(errors, /duplicate problem number 1/);
  assert.match(errors, /unknown paperId missing-paper/);
  assert.match(errors, /unknown prerequisite missing-prerequisite/);
});

test('reports malformed problem metadata JSON', t => {
  const fixture = createFixture();
  t.after(() => fs.rmSync(fixture.root, { recursive: true, force: true }));
  fs.writeFileSync(path.join(fixture.problemDir, 'meta.json'), '{');
  assert.ok(validateContent(fixture.root).errors.some(error => error.includes('invalid JSON')));
});
