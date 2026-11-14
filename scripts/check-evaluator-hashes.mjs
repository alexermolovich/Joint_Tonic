import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalSourceBytes, sha256 } from './canonical-source.mjs';

const defaultRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const hashLine = /^([ \t]*["']?evaluator_sha256["']?\s*:\s*["']?)([a-f0-9]{64})(["']?[ \t]*,?[ \t]*)$/gm;

/** Check declared hashes; --write repairs provenance and LF bytes, never tests. */
export function checkEvaluatorHashes(root = defaultRoot, { write = false } = {}) {
  const report = { problems: 0, undeclared: 0, normalizedEvaluators: 0, metadataRepairs: 0, blueprintRepairs: 0, issues: [] };
  for (const entry of fs.readdirSync(path.join(root, 'content/problems'), { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const directory = path.join(root, 'content/problems', entry.name);
    const evaluatorPath = path.join(directory, 'cases.py');
    const raw = fs.readFileSync(evaluatorPath);
    const canonical = canonicalSourceBytes('cases.py', raw);
    const digest = sha256(canonical);
    report.problems++;
    if (!raw.equals(canonical)) {
      report.normalizedEvaluators++;
      if (write) fs.writeFileSync(evaluatorPath, canonical);
      else report.issues.push(`${entry.name}: cases.py must use LF; run node scripts/check-evaluator-hashes.mjs --write before building or publishing.`);
    }

    const metaPath = path.join(directory, 'meta.json');
    const metaText = fs.readFileSync(metaPath, 'utf8');
    const meta = JSON.parse(metaText);
    const declared = meta.grading?.evaluator_sha256;
    if (declared === undefined) report.undeclared++; // Older packages use runtime-computed lineage.
    else if (declared !== digest) {
      report.metadataRepairs++;
      if (write) {
        const property = /("evaluator_sha256"\s*:\s*")[a-f0-9]{64}("+)/g;
        const matches = [...metaText.matchAll(property)];
        if (matches.length !== 1) throw new Error(`${entry.name}: repair the malformed or ambiguous evaluator hash manually.`);
        const updated = metaText.replace(property, (_match, prefix, suffix) => prefix + digest + suffix);
        if (JSON.parse(updated).grading?.evaluator_sha256 !== digest) throw new Error(`${entry.name}: could not locate the grading evaluator hash.`);
        fs.writeFileSync(metaPath, updated.replace(/\r\n/g, '\n'));
      }
      else report.issues.push(`${entry.name}: declared evaluator hash differs from canonical cases.py.`);
    }

    const blueprintPath = path.join(directory, 'blueprint.md');
    const blueprint = fs.readFileSync(blueprintPath, 'utf8');
    const frontMatter = blueprint.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
    if (frontMatter) {
      let changed = false;
      const updated = frontMatter[1].replace(hashLine, (line, prefix, old, suffix) => {
        if (old === digest) return line;
        changed = true;
        return prefix + digest + suffix;
      });
      if (changed) {
        report.blueprintRepairs++;
        if (write) fs.writeFileSync(blueprintPath, blueprint.replace(frontMatter[1], updated).replace(/\r\n/g, '\n'));
        else report.issues.push(`${entry.name}: blueprint evaluator hash differs from canonical cases.py.`);
      }
    }
  }
  return report;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const report = checkEvaluatorHashes(defaultRoot, { write: process.argv.includes('--write') });
  console.log(JSON.stringify(report, null, 2));
  if (report.issues.length) process.exitCode = 1;
}
