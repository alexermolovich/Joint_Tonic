begin;
create extension if not exists pgtap with schema extensions;
set local search_path=public,extensions;
select plan(16);
insert into auth.users(id,email,raw_user_meta_data) values('12000000-0000-0000-0000-000000000001','grader@joint-tonic.test','{}');
insert into public.problems(id,slug) values('22000000-0000-0000-0000-000000000001','grader-fixture');
insert into public.problem_versions(id,problem_id,version,title,difficulty,domain,content_sha256,evaluator_version,runtime_image_digest,metadata,state,published_at)
 values('32000000-0000-0000-0000-000000000001','22000000-0000-0000-0000-000000000001','1.0.0','Grader fixture','Easy','Geometry',repeat('0',64),repeat('1',64),'sha256:'||repeat('2',64),jsonb_build_object('fixture_sha256',repeat('1',64),'grading_protocol','data-only-functions-v1','grading',jsonb_build_object('seed',7)),'published',now());
insert into public.problem_versions(problem_id,version,title,difficulty,domain,content_sha256,evaluator_version,runtime_image_digest,metadata,state,published_at)
 values('22000000-0000-0000-0000-000000000001','2.0.0','Native fixture','Easy','Geometry',repeat('0',64),repeat('1',64),'sha256:'||repeat('2',64),jsonb_build_object('fixture_sha256',repeat('1',64),'grading_protocol','native-local-v1'),'published',now());
select ok(not has_function_privilege('authenticated','public.record_evaluation(jsonb)','execute'),'authenticated cannot submit trusted evidence');
select ok(not has_function_privilege('anon','public.record_evaluation(jsonb)','execute'),'anonymous cannot submit trusted evidence');
select ok(has_function_privilege('service_role','public.record_evaluation(jsonb)','execute'),'only trusted service can execute');
create temporary table payload(value jsonb);
insert into payload values(jsonb_build_object(
 'id','42000000-0000-0000-0000-000000000001','user_id','12000000-0000-0000-0000-000000000001','slug','grader-fixture','version','1.0.0','mode','submit','status','completed','code','return 1',
 'created_at','2026-11-14T00:00:00Z','started_at','2026-11-14T00:00:01Z','finished_at','2026-11-14T00:00:02Z',
 'result',jsonb_build_object('passed',true,'duration_ms',1000,'tests',jsonb_build_array(jsonb_build_object('passed',true))),
 'lineage',jsonb_build_object('grading_protocol','data-only-functions-v1','evaluator_sha256',repeat('1',64),'fixture_sha256',repeat('1',64),'runtime_image_digest','sha256:'||repeat('2',64),'seed',7)));
grant select on payload to service_role;
set local role service_role;
select is(record_evaluation((select value from payload))->>'duplicate','false','first terminal evaluation persisted');
select is(record_evaluation((select value from payload))->>'duplicate','true','exact retry is idempotent');
select is((select count(*)::integer from public.progress),1,'one verified solve created');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{code}','"changed"'))$t$,'23514',null,'immutable job cannot change source');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{lineage,runtime_image_digest}',to_jsonb('sha256:'||repeat('3',64))))$t$,'23514',null,'mismatched runtime cannot establish progress');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{result,passed}','false'))$t$,'23514',null,'aggregate result must match trusted checks');
select is(record_evaluation((select value from payload)||'{"id":"42000000-0000-0000-0000-000000000002","mode":"run"}'::jsonb)->>'persisted','true','public Run history can be recorded');
select is((select count(*)::integer from public.submissions),1,'public Run never creates a scored submission');
select is(record_evaluation((select value from payload)||jsonb_build_object('id','42000000-0000-0000-0000-000000000003','result',jsonb_build_object('passed',false,'duration_ms',10,'tests',jsonb_build_array(jsonb_build_object('passed',false)))))->>'persisted','true','failed Submit remains inspectable');
select is((select count(*)::integer from public.progress),1,'failed Submit never adds verified progress');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{version}','"2.0.0"'))$t$,'23514',null,'native catalog contract cannot claim data-only qualification');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{lineage,seed}','8'))$t$,'23514',null,'seed must match the published grading contract');
select throws_ok($t$select record_evaluation(jsonb_set((select value from payload),'{result,error}','"runtime failed"'))$t$,'23514',null,'passing result cannot contain a runtime error');
reset role;
select * from finish();
rollback;
