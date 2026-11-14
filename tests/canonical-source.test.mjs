import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalSourceBytes, catalogSourceIdentity, sha256 } from '../scripts/canonical-source.mjs';
import { checkEvaluatorHashes } from '../scripts/check-evaluator-hashes.mjs';

function temporary(t) {
  const parent = fs.realpathSync(os.tmpdir());
  const directory = fs.mkdtempSync(path.join(parent, 'joint-tonic-source-'));
  t.after(() => {
    const resolved = fs.realpathSync(directory);
    assert.equal(path.dirname(resolved), parent);
    assert.match(path.basename(resolved), /^joint-tonic-source-/);
    fs.rmSync(resolved, { recursive: true, force: true });
  });
  return directory;
}

test('canonical text preserves Unicode, BOM and terminal-newline identity; binary bytes remain exact', () => {
  const source = Buffer.from('\ufeff# café\r\nvalue = 1\r\n');
  const before = Buffer.from(source);
  assert.equal(canonicalSourceBytes('cases.py', source).toString(), '\ufeff# café\nvalue = 1\n');
  assert.deepEqual(source, before);
  assert.equal(canonicalSourceBytes('cases.py', Buffer.from('a\rb\r')).toString(), 'a\nb\n');
  assert.notEqual(sha256(canonicalSourceBytes('cases.py', Buffer.from('x\n'))), sha256(canonicalSourceBytes('cases.py', Buffer.from('x'))));
  assert.deepEqual(canonicalSourceBytes('fixture.bin', source), source);
  assert.deepEqual(canonicalSourceBytes('image.png', Buffer.from([0, 13, 10, 255])), Buffer.from([0, 13, 10, 255]));
  assert.throws(() => canonicalSourceBytes('cases.py', Buffer.from([255])), /valid UTF-8/);
});

test('LF and CRLF source manifests agree, but runtime evaluator canonicality and real content changes remain visible', t => {
  const directory = temporary(t);
  fs.writeFileSync(path.join(directory, 'cases.py'), '# original\nassert 1 == 1\n');
  fs.writeFileSync(path.join(directory, 'theory.md'), '# Robot\nOriginal explanation.\n');
  fs.writeFileSync(path.join(directory, 'fixture.bin'), Buffer.from([0, 13, 10, 255]));
  const linux = catalogSourceIdentity(directory);
  for (const name of ['cases.py', 'theory.md']) fs.writeFileSync(path.join(directory, name), fs.readFileSync(path.join(directory, name), 'utf8').replace(/\n/g, '\r\n'));
  const windows = catalogSourceIdentity(directory);
  assert.deepEqual(windows.sourceManifest, linux.sourceManifest);
  assert.equal(windows.contentSha256, linux.contentSha256);
  assert.equal(windows.evaluatorSha256, linux.evaluatorSha256);
  assert.equal(linux.evaluatorIsCanonical, true);
  assert.equal(windows.evaluatorIsCanonical, false);
  fs.appendFileSync(path.join(directory, 'cases.py'), '# changed\r\n');
  assert.notEqual(catalogSourceIdentity(directory).contentSha256, linux.contentSha256);
  fs.writeFileSync(path.join(directory, 'cases.py'), '# original\nassert 1 == 1\n');
  fs.writeFileSync(path.join(directory, 'fixture.bin'), Buffer.from([0, 10, 255]));
  assert.notEqual(catalogSourceIdentity(directory).contentSha256, linux.contentSha256);
});

test('provenance repair normalizes evaluator bytes and declared hashes without changing versions, contracts or unrelated body text', t => {
  const root = temporary(t);
  const directory = path.join(root, 'content/problems/example');
  fs.mkdirSync(directory, { recursive: true });
  const raw = Buffer.from('def check():\r\n    assert 1 == 1\r\n');
  const canonical = canonicalSourceBytes('cases.py', raw);
  const previous = sha256(raw);
  fs.writeFileSync(path.join(directory, 'cases.py'), raw);
  const meta = { version: '1.0.0', entrypoint: 'solve', grading: { seed: 42, evaluator_sha256: previous } };
  const metaText = JSON.stringify(meta).replace('"seed":42', '"seed":42,"rtol":1e-09');
  fs.writeFileSync(path.join(directory, 'meta.json'), metaText);
  fs.writeFileSync(path.join(directory, 'blueprint.md'), `---\r\ngrading:\r\n  evaluator_sha256: ${previous}\r\n---\r\nOriginal contract, version 1.0.0.\r\n`);
  const before = checkEvaluatorHashes(root);
  assert.equal(before.metadataRepairs, 1);
  assert.equal(before.blueprintRepairs, 1);
  assert.equal(before.normalizedEvaluators, 1);
  assert.equal(before.issues.length, 3);
  checkEvaluatorHashes(root, { write: true });
  assert.deepEqual(fs.readFileSync(path.join(directory, 'cases.py')), canonical);
  assert.equal(fs.readFileSync(path.join(directory, 'meta.json'), 'utf8'), metaText.replace(previous, sha256(canonical)));
  assert.equal(fs.readFileSync(path.join(directory, 'blueprint.md'), 'utf8'), `---\ngrading:\n  evaluator_sha256: ${sha256(canonical)}\n---\nOriginal contract, version 1.0.0.\n`);
  assert.deepEqual(checkEvaluatorHashes(root).issues, []);
});

test('checked-in evaluators use canonical bytes and every declared provenance hash matches', () => {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const report = checkEvaluatorHashes(root);
  assert.ok(report.problems > 0);
  assert.deepEqual(report.issues, []);
});

test('every checked-in problem source can be hashed with strict UTF-8 validation', () => {
  const problems = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../content/problems');
  const directories = fs.readdirSync(problems, { withFileTypes: true }).filter(entry => entry.isDirectory());
  assert.ok(directories.length > 0);
  for (const entry of directories) {
    const directory = path.join(problems, entry.name);
    assert.doesNotThrow(() => catalogSourceIdentity(directory), entry.name);
  }
  // These legacy CP1252 notes must preserve their intended Unicode characters.
  for (const [slug, phrase] of [
    ['aggregate-policy-returns', 'policy\u2019s'],
    ['compare-pipeline-measurements', 'request\u2019s'],
    ['extract-elastic-subnetwork', 'O(L C\u00b2 K\u00b2)'],
    ['finite-difference-gradient-check', 'O(MD\u00b2)'],
    ['pareto-edge-model-selection', 'O(N\u00b2)'],
    ['reuse-tensor-buffers', 'O(N\u00b2)'],
    ['robot-episode-confidence-intervals', 'metric\u2019s'],
    ['seed-deterministic-evaluation', 'episode\u2019s'],
  ]) {
    const bytes = fs.readFileSync(path.join(problems, slug, 'solution.md'));
    assert.ok(bytes.toString('utf8').includes(phrase), slug);
    assert.deepEqual(bytes, canonicalSourceBytes('solution.md', bytes), slug);
  }
});
