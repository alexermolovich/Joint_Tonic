import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import {fileURLToPath} from 'node:url';
import {parsePaperFlow,paperSectionId} from '../apps/web/src/lib/paper-flow.ts';
process.chdir(path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'));
const walk=(d:string):string[]=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):e.name.endsWith('.md')?[path.join(d,e.name)]:[]);
const catalog=fs.readdirSync('content/problems').flatMap(slug=>{const f=path.join('content/problems',slug,'meta.json');return fs.existsSync(f)?[JSON.parse(fs.readFileSync(f,'utf8'))]:[];});
const cards=walk('research/papers').map(file=>({file,...matter(fs.readFileSync(file,'utf8')),id:path.basename(file,'.md')}));
const canonical=new Map<string,typeof cards>();for(const c of cards){const key=String(c.data.primary_url).trim().replace(/\/$/,'');if(!canonical.has(key))canonical.set(key,[]);canonical.get(key)!.push(c);}
const projects=new Map(cards.map(c=>[c.id,c]));
const files=walk('content/tracks/papers');const errors:string[]=[];let nodes=0,links=0,proposed=0;
const check=(condition:boolean,message:string)=>{if(!condition)errors.push(message);};
check(files.length===canonical.size,'Track count mismatches canonical source count');
const index=fs.readFileSync('content/PAPER_TRACKS.md','utf8');
for(const [url,group] of canonical){
  const id=group[0].id,file='content/tracks/papers/paper-'+id+'.md';
  check(fs.existsSync(file),'Missing track '+id);if(!fs.existsSync(file))continue;
  const {data,content}=matter(fs.readFileSync(file,'utf8'));
  check(data.primary_url===url&&data.paper_id===id,'Identity mismatch '+id);
  const integrationFile='content/paper-projects/'+id+'/meta.json';
  const integration=fs.existsSync(integrationFile)?JSON.parse(fs.readFileSync(integrationFile,'utf8')):null;
  check(integration ? data.status==='bounded-integration-available'&&data.integration_status==='runnable'&&data.assessment_status==='runnable'&&data.integration_problem_slug===integration.integrationProblemSlug&&catalog.some(p=>p.slug===integration.integrationProblemSlug) : data.status==='planned'&&data.integration_status==='proposed'&&data.assessment_status==='proposed','Completion claim '+id);
  check(index.includes('(tracks/papers/paper-'+id+'.md)'),'Missing index entry '+id);
  const expected=group.flatMap(c=>c.data.execution_flow.nodes.map((n:any)=>({card:c.id,node:n.id})));
  check(JSON.stringify(expected)===JSON.stringify(data.source_flow_nodes),'Missing or reordered source identity '+id);
  check(expected.length===data.source_flow_node_count,'Wrong node count '+id);nodes+=expected.length;
  for(const c of group){
    const flow=parsePaperFlow(c.data.execution_flow,c.content,catalog.map(p=>p.slug),catalog)!;
    for(const n of flow.nodes){
      check(content.includes('<!-- source-flow: '+c.id+'#'+n.id+' -->'),'Missing mechanism '+c.id+'#'+n.id);
      for(const slug of n.problem_slugs)check(content.includes('](/problems/'+slug+')'),'Missing runnable association '+id+'/'+slug);
      for(const title of n.planned_problems||[]){proposed++;check(content.includes('**Proposed component, not runnable:** '+title+'.'),'Missing proposed association '+id+'/'+title);}
    }
  }
  for(const heading of ['Orientation and scope','Prerequisites and diagnostic','Ordered mechanisms and component tasks','Integration exercise','Evaluation and failure analysis','Reproducibility deliverable'])check(content.includes('## '+heading+'\n'),'Missing section '+id+'/'+heading);
  for(const heading of ['Integration exercise','Evaluation and failure analysis','Reproducibility deliverable']){
    const section=content.split('## '+heading+'\n')[1]?.split('\n## ')[0]||'';
    check(section.includes(integration?'Runnable':'Proposed'),'Section status missing '+id+'/'+heading);
    check(!/\]\((?:\.\.|content|research)/.test(section),'Local URL in UI section '+id+'/'+heading);
  }
  check(!content.includes('undefined')&&!content.includes('[object Object]'),'Serialization text leak '+id);
  for(const match of content.matchAll(/\]\(([^)]+)\)/g)){
    links++;const target=match[1];if(/^https?:\/\//.test(target))continue;
    if(target.startsWith('/problems/')){check(catalog.some(p=>p.slug===target.slice(10)),'Unknown problem '+target);continue;}
    if(target.startsWith('/projects/')){
      const [projectId,anchor]=target.slice(10).split('#');const c=projects.get(projectId);
      check(!!c,'Unknown project '+target);if(c&&anchor)check([...c.content.matchAll(/^#{2,3}\s+(.+)$/gm)].some(m=>paperSectionId(m[1].trim())===anchor),'Missing project anchor '+target);
      continue;
    }
    check(fs.existsSync(path.resolve(path.dirname(file),target)),'Broken local link '+file+'/'+target);
  }
}
console.log(JSON.stringify({tracks:files.length,sourceCards:cards.length,sourceNodes:nodes,plannedStageAssociations:proposed,checkedLinks:links,errors},null,2));
if(errors.length)process.exitCode=1;
