begin;

-- This RPC is called only by the isolated evaluator control plane. The browser
-- has neither EXECUTE permission nor permission to write evaluation/progress rows.
create function public.record_evaluation(p_job jsonb)
returns jsonb language plpgsql security invoker set search_path = '' as $$
declare
  job_uuid uuid;
  owner_uuid uuid;
  version_row public.problem_versions%rowtype;
  existing public.jobs%rowtype;
  created_time timestamptz;
  started_time timestamptz;
  finished_time timestamptz;
  safe_result jsonb;
  lineage jsonb;
  total integer;
  passed_total integer;
  verdict_value text;
  submission_uuid uuid;
  duration_value numeric;
begin
  if jsonb_typeof(p_job) is distinct from 'object' or octet_length(p_job::text)>524288 then
    raise exception 'invalid evaluation envelope' using errcode='22023';
  end if;
  job_uuid := (p_job->>'id')::uuid;
  owner_uuid := (p_job->>'user_id')::uuid;
  created_time := (p_job->>'created_at')::timestamptz;
  started_time := (p_job->>'started_at')::timestamptz;
  finished_time := (p_job->>'finished_at')::timestamptz;
  lineage := p_job->'lineage';
  if job_uuid is null or owner_uuid is null or created_time is null or started_time is null or finished_time is null
     or not isfinite(created_time) or not isfinite(started_time) or not isfinite(finished_time)
     or started_time<created_time or finished_time<started_time
     or p_job->>'mode' is null or p_job->>'mode' not in ('run','submit')
     or p_job->>'status' is null or p_job->>'status' not in ('completed','failed')
     or jsonb_typeof(p_job->'code') is distinct from 'string' or octet_length(p_job->>'code') not between 1 and 100000
     or jsonb_typeof(p_job->'result') is distinct from 'object'
     or jsonb_typeof(lineage) is distinct from 'object'
     or lineage->>'grading_protocol' is distinct from 'data-only-functions-v1'
     or lineage->>'evaluator_sha256' is null or lineage->>'evaluator_sha256' !~ '^[a-f0-9]{64}$'
     or lineage->>'fixture_sha256' is null or lineage->>'fixture_sha256' !~ '^[a-f0-9]{64}$'
     or lineage->>'runtime_image_digest' is null or lineage->>'runtime_image_digest' !~ '^sha256:[a-f0-9]{64}$'
     or jsonb_typeof(lineage->'seed') is distinct from 'number' or lineage->>'seed' !~ '^[0-9]{1,18}$' then
    raise exception 'invalid trusted evaluation contract' using errcode='22023';
  end if;
  select v.* into version_row from public.problem_versions v join public.problems p on p.id=v.problem_id
    where p.slug=p_job->>'slug' and v.version=p_job->>'version' and v.published_at is not null;
  if version_row.id is null or version_row.runtime_image_digest is distinct from lineage->>'runtime_image_digest'
     or version_row.evaluator_version is distinct from lineage->>'evaluator_sha256'
     or version_row.metadata->>'fixture_sha256' is distinct from lineage->>'fixture_sha256'
     or version_row.metadata->>'grading_protocol' is distinct from lineage->>'grading_protocol'
     or (version_row.metadata->'grading' ? 'seed' and version_row.metadata->'grading'->'seed' is distinct from lineage->'seed') then
    raise exception 'evaluation lineage does not match published content' using errcode='23514';
  end if;
  safe_result := (p_job->'result') || jsonb_build_object('lineage',lineage);
  if octet_length(safe_result::text)>262144 then raise exception 'result too large' using errcode='22023'; end if;
  if p_job->>'status'='completed' then
    if jsonb_typeof(safe_result->'passed') is distinct from 'boolean' or jsonb_typeof(safe_result->'tests') is distinct from 'array'
       or jsonb_array_length(safe_result->'tests') not between 1 and 1000 then
      raise exception 'completed evaluation needs bounded test evidence' using errcode='23514';
    end if;
    if exists(select 1 from jsonb_array_elements(safe_result->'tests') t where jsonb_typeof(t->'passed') is distinct from 'boolean') then
      raise exception 'test verdict must be boolean' using errcode='23514';
    end if;
    select count(*)::integer,count(*) filter(where t->>'passed'='true')::integer into total,passed_total from jsonb_array_elements(safe_result->'tests') t;
    if (safe_result->>'passed')::boolean is distinct from (total=passed_total) then
      raise exception 'aggregate verdict does not match test evidence' using errcode='23514';
    end if;
    if total=passed_total and coalesce(safe_result->>'error','')<>'' then
      raise exception 'passing evaluation cannot include an error' using errcode='23514';
    end if;
    verdict_value := case when total=passed_total then 'passed' else 'failed' end;
  else
    safe_result := safe_result || '{"passed":false}'::jsonb;
    total:=0; passed_total:=0; verdict_value:='error';
  end if;
  if jsonb_typeof(safe_result->'duration_ms') is distinct from 'number' then raise exception 'duration required' using errcode='22023'; end if;
  duration_value := (safe_result->>'duration_ms')::numeric;
  if duration_value<0 or duration_value>1000000000 then raise exception 'duration outside bounds' using errcode='22023'; end if;

  -- Serializes duplicate deliveries before the immutable insert/derived writes.
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(job_uuid::text,0));
  select * into existing from public.jobs where id=job_uuid;
  if existing.id is not null then
    if existing.user_id is distinct from owner_uuid or existing.problem_version_id is distinct from version_row.id
       or existing.code is distinct from p_job->>'code' or existing.mode is distinct from p_job->>'mode'
       or existing.status is distinct from p_job->>'status' or existing.created_at is distinct from created_time
       or existing.started_at is distinct from started_time or existing.finished_at is distinct from finished_time
       or existing.result is distinct from safe_result then
      raise exception 'job identifier already belongs to a different immutable evaluation' using errcode='23514';
    end if;
    return jsonb_build_object('id',job_uuid,'persisted',true,'duplicate',true);
  end if;
  insert into public.jobs(id,user_id,problem_version_id,mode,status,code,correlation_id,created_at,started_at,finished_at,result,error)
    values(job_uuid,owner_uuid,version_row.id,p_job->>'mode',p_job->>'status',p_job->>'code',job_uuid,created_time,started_time,finished_time,safe_result,left(safe_result->>'error',2000));
  if p_job->>'mode'='submit' then
    insert into public.submissions(user_id,problem_version_id,job_id,created_at)
      values(owner_uuid,version_row.id,job_uuid,created_time) returning id into submission_uuid;
    insert into public.evaluations(submission_id,verdict,evaluator_version,runtime_image_digest,fixture_sha256,seed,duration_ms,passed_count,total_count,summary,correlation_id,created_at)
      values(submission_uuid,verdict_value,lineage->>'evaluator_sha256',lineage->>'runtime_image_digest',lineage->>'fixture_sha256',(lineage->>'seed')::bigint,duration_value,passed_total,total,safe_result,job_uuid,finished_time);
    if verdict_value='passed' then
      insert into public.progress(user_id,problem_version_id,solved_at,submission_id)
        values(owner_uuid,version_row.id,finished_time,submission_uuid) on conflict(user_id,problem_version_id) do nothing;
    end if;
  end if;
  return jsonb_build_object('id',job_uuid,'persisted',true,'duplicate',false);
end;
$$;
revoke all on function public.record_evaluation(jsonb) from public,anon,authenticated;
grant execute on function public.record_evaluation(jsonb) to service_role;
comment on function public.record_evaluation(jsonb) is 'Atomic terminal evaluator evidence, idempotent immutable history and first verified solve; service-role control-plane caller only.';
commit;
