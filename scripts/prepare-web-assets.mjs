import { cpSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const target = path.join(root, 'apps/web/public/monaco/vs');
mkdirSync(path.dirname(target), { recursive: true });
cpSync(path.join(root, 'node_modules/monaco-editor/min/vs'), target, { recursive: true });
