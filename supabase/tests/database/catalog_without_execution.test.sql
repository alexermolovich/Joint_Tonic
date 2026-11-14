begin;
select plan(5);

insert into public.problems(id,slug) values ('00000000-0000-4000-8000-000000000901','catalog-only-test');

select lives_ok($test$
  insert into public.problem_versions(id,problem_id,version,title,difficulty,domain,metadata,content_sha256,evaluator_version,state,published_at)
  values ('00000000-0000-4000-8000-000000000902','00000000-0000-4000-8000-000000000901','1.0.0','Catalog-only test','Easy','test','{"grading_protocol":"unavailable"}',repeat('a',64),repeat('b',64),'published',now())
$test$, 'explicitly unavailable catalog version can be published without an image');

select throws_ok($test$
  insert into public.problem_versions(problem_id,version,title,difficulty,domain,metadata,content_sha256,evaluator_version,state,published_at)
  values ('00000000-0000-4000-8000-000000000901','1.0.1','Missing protocol','Easy','test','{}',repeat('a',64),repeat('b',64),'published',now())
$test$, '23514', null, 'missing protocol cannot bypass the runtime requirement through NULL');

select throws_ok($test$
  insert into public.problem_versions(problem_id,version,title,difficulty,domain,metadata,content_sha256,evaluator_version,state,published_at)
  values ('00000000-0000-4000-8000-000000000901','1.0.2','Execution without image','Easy','test','{"grading_protocol":"data-only-functions-v1"}',repeat('a',64),repeat('b',64),'published',now())
$test$, '23514', null, 'executable protocol still requires an actual runtime identity');

select throws_ok($test$
  update public.problem_versions set runtime_image_digest='sha256:'||repeat('c',64),metadata='{"grading_protocol":"data-only-functions-v1"}'
  where id='00000000-0000-4000-8000-000000000902'
$test$, '55000', null, 'published catalog identity cannot be silently upgraded to execution');

select throws_ok($test$
  select public.record_evaluation(jsonb_build_object(
    'id','00000000-0000-4000-8000-000000000903','user_id','00000000-0000-4000-8000-000000000904',
    'slug','catalog-only-test','version','1.0.0','mode','submit','status','completed','code','pass',
    'created_at','2026-11-14T00:00:00Z','started_at','2026-11-14T00:00:00Z','finished_at','2026-11-14T00:00:01Z',
    'result',jsonb_build_object('passed',true,'tests',jsonb_build_array(jsonb_build_object('passed',true)),'duration_ms',1),
    'lineage',jsonb_build_object('grading_protocol','data-only-functions-v1','evaluator_sha256',repeat('b',64),
      'fixture_sha256',repeat('b',64),'runtime_image_digest','sha256:'||repeat('c',64),'seed',1)))
$test$, '23514', 'evaluation lineage does not match published content', 'catalog-only version rejects trusted evaluation evidence before inserting any score');

select * from finish();
rollback;
