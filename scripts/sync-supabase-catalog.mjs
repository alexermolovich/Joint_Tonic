/** Prepare public catalog rows; --apply is the explicit remote-write switch. */
import fs from 'node:fs';
import path from 'node:path';
import { catalogSourceIdentity } from './canonical-source.mjs';
import { prepareCatalogWorkspace } from './catalog-seed.mjs';
const args=process.argv.slice(2);
const catalogOnly=args.includes('--catalog-only');
if(catalogOnly&&args.some(a=>a.startsWith('--runtime-image-digest=')))throw new Error('Catalog-only publication must not assign an execution image.');
if(args.includes('--prepare-cli-seed')&&(!catalogOnly||args.includes('--apply')))throw new Error('CLI seed preparation requires --catalog-only and cannot be combined with --apply.');
const digest=catalogOnly?null:args.find(a=>a.startsWith('--runtime-image-digest='))?.split('=')[1]||process.env.WORKER_RUNTIME_IMAGE_DIGEST;
if(!catalogOnly&&(!/^sha256:[a-f0-9]{64}$/.test(digest||'')||/^sha256:0+$/.test(digest)))throw new Error('Supply an actual built worker image digest, or use --catalog-only to publish account-storage identities with execution unavailable. No placeholder is generated.');
const catalog=fs.readdirSync('content/problems').sort().map(slug=>{
 const dir=path.join('content/problems',slug);const meta=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const source=catalogSourceIdentity(dir);
 if(!source.evaluatorIsCanonical)throw new Error(`${slug}/cases.py must use LF so actual worker lineage matches the catalog. Run node scripts/check-evaluator-hashes.mjs --write, then rebuild the worker image before publishing.`);
 const evaluator=source.evaluatorSha256;
 if(meta.grading?.evaluator_sha256!==undefined&&meta.grading.evaluator_sha256!==evaluator)throw new Error(`${slug}: declared evaluator hash is stale. Run node scripts/check-evaluator-hashes.mjs --write and review the provenance correction before publishing.`);
 const contract=meta.execution_contract;
 const qualified=contract?.protocol==='data-only-functions-v1'&&contract.semantics==='value-only'&&typeof contract.reviewed_by==='string'&&contract.reviewed_by.trim().length>0;
 return {slug,version:{version:meta.version,title:meta.title,difficulty:meta.difficulty,domain:meta.domain,topics:meta.topics||[],paper_ids:meta.paperIds||[],metadata:{...meta,fixture_sha256:evaluator,grading_protocol:catalogOnly?'unavailable':qualified?'data-only-functions-v1':'native-local-v1',catalog_source_digest:source.contentSha256},content_sha256:source.contentSha256,evaluator_version:evaluator,runtime_image_digest:digest,state:'published'}};
});
if(!args.includes('--apply')){
 fs.mkdirSync('.local',{recursive:true});fs.writeFileSync('.local/supabase-catalog-plan.json',JSON.stringify(catalog,null,2)+'\n');
 console.log(JSON.stringify({event:'catalog_plan_ready',count:catalog.length,path:'.local/supabase-catalog-plan.json',applied:false}));
 if(args.includes('--prepare-cli-seed'))console.log(JSON.stringify({event:'catalog_cli_workspace_ready',path:prepareCatalogWorkspace(catalog),applied:false}));
}else{
 const url=process.env.SUPABASE_URL||process.env.NEXT_PUBLIC_SUPABASE_URL;
 const key=process.env.SUPABASE_SECRET_KEY||process.env.SUPABASE_SERVICE_ROLE_KEY;
 if(!url||!key)throw new Error('Apply requires SUPABASE_URL and a server-only SUPABASE_SECRET_KEY or SUPABASE_SERVICE_ROLE_KEY. Never use a NEXT_PUBLIC secret.');
 const endpoint=new URL(url);if(endpoint.protocol!=='https:'&&!(endpoint.protocol==='http:'&&['localhost','127.0.0.1','[::1]'].includes(endpoint.hostname)))throw new Error('Supabase endpoint must use HTTPS or local loopback HTTP.');
 if(endpoint.username||endpoint.password)throw new Error('Supabase endpoint must not contain credentials.');
 const headers={apikey:key,Authorization:`Bearer ${key}`,'Content-Type':'application/json'};
 async function request(resource,options={}){
  const response=await fetch(`${endpoint.origin}/rest/v1/${resource}`,{...options,headers:{...headers,...options.headers},signal:AbortSignal.timeout(15000)});
  if(!response.ok)throw new Error(`Catalog request failed (${response.status}). Verify migrations and server credentials; response is intentionally not logged.`);
  return response.status===204?null:response.json();
 }
 let created=0,existing=0;
 for(const item of catalog){
  const problems=await request('problems?on_conflict=slug',{method:'POST',headers:{Prefer:'resolution=merge-duplicates,return=representation'},body:JSON.stringify({slug:item.slug})});
  const problemId=problems[0].id;
  const prior=await request(`problem_versions?problem_id=eq.${problemId}&version=eq.${encodeURIComponent(item.version.version)}&select=id,content_sha256,evaluator_version,runtime_image_digest,state`);
  if(prior.length){
   const old=prior[0];if(old.content_sha256!==item.version.content_sha256||old.evaluator_version!==item.version.evaluator_version||old.runtime_image_digest!==digest||old.state==='draft')throw new Error(`Immutable version conflict for ${item.slug}@${item.version.version}. Review a new semantic version; existing content was not overwritten.`);
   existing++;continue;
  }
  await request('problem_versions',{method:'POST',headers:{Prefer:'return=representation'},body:JSON.stringify({...item.version,problem_id:problemId,published_at:new Date().toISOString()})});created++;
 }
 console.log(JSON.stringify({event:'catalog_sync_complete',created,existing,total:catalog.length}));
}
