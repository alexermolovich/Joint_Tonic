import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const textExtensions = new Set(['.py', '.md', '.json', '.txt', '.yaml', '.yml', '.toml', '.csv', '.ts', '.tsx', '.js', '.mjs', '.cjs', '.css', '.html', '.svg', '.xml', '.sql', '.sh', '.ps1']);
const textNames = new Set(['LICENSE', 'NOTICE', '.gitattributes', '.gitignore']);
export const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

/** Normalize source-text line endings only. Binary/unknown formats stay exact. */
export function canonicalSourceBytes(name, bytes) {
  const input = Buffer.from(bytes);
  if (!textExtensions.has(path.extname(name).toLowerCase()) && !textNames.has(path.basename(name))) return input;
  try { new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(input); }
  catch { throw new Error(`${name}: source text must be valid UTF-8.`); }
  // Work on bytes so Unicode normalization, BOMs and final newlines stay intact.
  return Buffer.from(input.toString('utf8').replace(/\r\n?/g, '\n'), 'utf8');
}

export function catalogSourceIdentity(directory) {
  const names = fs.readdirSync(directory).filter(name => fs.statSync(path.join(directory, name)).isFile()).sort();
  const sourceManifest = names.map(name => [name, sha256(canonicalSourceBytes(name, fs.readFileSync(path.join(directory, name))))]);
  const rawEvaluator = fs.readFileSync(path.join(directory, 'cases.py'));
  const evaluator = canonicalSourceBytes('cases.py', rawEvaluator);
  return {
    sourceManifest,
    contentSha256: sha256(JSON.stringify(sourceManifest)),
    evaluatorSha256: sha256(evaluator),
    evaluatorIsCanonical: rawEvaluator.equals(evaluator),
  };
}
