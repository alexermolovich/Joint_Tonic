import { cpSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Vercel's project root is the repository (package.json lives here). Its Next
// builder collects public/ here even when build output is apps/web/.next.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
cpSync(path.join(root, 'apps/web/public'), path.join(root, 'public'), { recursive: true });
