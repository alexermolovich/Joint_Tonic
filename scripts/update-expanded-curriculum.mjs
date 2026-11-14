import fs from 'node:fs';
import path from 'node:path';

const start='<!-- reviewed-expansion:start -->', end='<!-- reviewed-expansion:end -->';
const capstones=new Set(fs.readdirSync('content/capstones').map(slug=>JSON.parse(fs.readFileSync(path.join('content/capstones',slug,'meta.json'),'utf8')).integrationProblemSlug));
const problems=fs.readdirSync('content/problems').flatMap(slug=>{
  const file=path.join('content/problems',slug,'meta.json');
  return fs.existsSync(file)?[JSON.parse(fs.readFileSync(file,'utf8'))]:[];
}).filter(problem=>problem.number>=500&&!capstones.has(problem.slug)).sort((a,b)=>a.number-b.number);
const groups=new Map();
for(const problem of problems){if(!groups.has(problem.domain))groups.set(problem.domain,[]);groups.get(problem.domain).push(problem);}
const lines=[start,'','## 7. Reviewed paper-library expansion','',
  'The user authorized the remaining paper backlog after the original 190-problem curriculum. This generated section lists reviewed additions with published evaluators. The complete proposed inventory and source associations remain in [the implementation backlog](research/IMPLEMENTATION_BACKLOG.md); a proposed title is not a completed exercise.',''];
let index=0;
for(const [domain,items] of groups){lines.push(`### 7.${++index} ${domain}`,'');for(const item of items)lines.push(`- \`[paper]\` ${item.title}`);lines.push('');}
lines.push(end);
let document=fs.readFileSync('CURRICULUM.md','utf8');
if(document.includes(start))document=document.slice(0,document.indexOf(start))+lines.join('\n')+document.slice(document.indexOf(end)+end.length);
else document=document.replace('## 7. Maintenance rules',lines.join('\n')+'\n\n## 8. Maintenance rules');
fs.writeFileSync('CURRICULUM.md',document);
console.log(JSON.stringify({reviewedExpansion:problems.length,capstones:capstones.size}));
