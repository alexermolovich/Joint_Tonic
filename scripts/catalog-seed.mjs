import fs from 'node:fs';
import path from 'node:path';

/** A transactionally applied catalog-only seed; no credentials are embedded. */
export function catalogSeedSql(catalog) {
  if(!Array.isArray(catalog)||!catalog.length)throw new Error('A nonempty reviewed catalog is required.');
  for(const item of catalog){
    if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(item.slug)||item.version?.runtime_image_digest!==null||item.version?.metadata?.grading_protocol!=='unavailable'||item.version?.state!=='published')throw new Error('CLI seed supports only explicit catalog-only publication.');
  }
  const payload=JSON.stringify(catalog),tag='$joint_tonic_catalog_payload$';
  if(payload.includes(tag)||payload.includes('$joint_tonic_catalog_seed$'))throw new Error('Catalog contains a reserved SQL delimiter.');
  return `-- Generated catalog-only identities. Review the plan before remote application.
begin;
do $joint_tonic_catalog_seed$
declare
  item jsonb;
  v jsonb;
  problem_uuid uuid;
  prior public.problem_versions%rowtype;
begin
  for item in select value from jsonb_array_elements(${tag}${payload}${tag}::jsonb)
  loop
    v := item->'version';
    if v->>'runtime_image_digest' is not null or v->'metadata'->>'grading_protocol' is distinct from 'unavailable'
       or v->>'state' is distinct from 'published' then
      raise exception 'catalog-only seed cannot enable execution';
    end if;
    insert into public.problems(slug) values(item->>'slug') on conflict(slug) do nothing;
    select id into problem_uuid from public.problems where slug=item->>'slug';
    select * into prior from public.problem_versions where problem_id=problem_uuid and version=v->>'version';
    if found then
      if prior.content_sha256 is distinct from v->>'content_sha256'
         or prior.evaluator_version is distinct from v->>'evaluator_version'
         or prior.runtime_image_digest is not null
         or prior.metadata->>'grading_protocol' is distinct from 'unavailable'
         or prior.state='draft' then
        raise exception 'immutable catalog version conflict for %@%', item->>'slug', v->>'version';
      end if;
    else
      insert into public.problem_versions(problem_id,version,title,difficulty,domain,topics,paper_ids,metadata,
        content_sha256,evaluator_version,runtime_image_digest,state,published_at)
      values(problem_uuid,v->>'version',v->>'title',v->>'difficulty',v->>'domain',
        array(select jsonb_array_elements_text(v->'topics')),array(select jsonb_array_elements_text(v->'paper_ids')),
        v->'metadata',v->>'content_sha256',v->>'evaluator_version',null,'published',now());
    end if;
  end loop;
end;
$joint_tonic_catalog_seed$;
commit;
`;
}

export function prepareCatalogWorkspace(catalog,root=process.cwd()) {
  const destination=path.join(root,'.local/supabase-catalog-publish');
  const directory=path.join(destination,'supabase');
  fs.mkdirSync(path.join(directory,'migrations'),{recursive:true});
  const migrationNames=fs.readdirSync(path.join(root,'supabase/migrations')).filter(n=>n.endsWith('.sql')).sort();
  for(const old of fs.readdirSync(path.join(directory,'migrations')))if(!migrationNames.includes(old))throw new Error('Unexpected old migration in generated catalog workspace: '+old);
  for(const name of migrationNames)fs.copyFileSync(path.join(root,'supabase/migrations',name),path.join(directory,'migrations',name));
  fs.writeFileSync(path.join(directory,'config.toml'),'project_id = "joint-tonic-catalog-publish"\n\n[db]\nmajor_version = 17\n\n[db.seed]\nenabled = true\nsql_paths = ["./seed.sql"]\n');
  fs.writeFileSync(path.join(directory,'seed.sql'),catalogSeedSql(catalog));
  return path.relative(root,destination).split(path.sep).join('/');
}
