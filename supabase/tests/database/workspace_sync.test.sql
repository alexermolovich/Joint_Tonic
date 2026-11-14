begin;
create extension if not exists pgtap with schema extensions;
set local search_path=public,extensions;
select plan(10);
insert into auth.users(id,email,raw_user_meta_data) values
 ('11000000-0000-0000-0000-000000000001','sync-a@joint-tonic.test','{}'),
 ('11000000-0000-0000-0000-000000000002','sync-b@joint-tonic.test','{}');
insert into public.problems(id,slug) values('21000000-0000-0000-0000-000000000001','sync-fixture');
insert into public.problem_versions(id,problem_id,version,title,difficulty,domain,content_sha256,evaluator_version,runtime_image_digest,state,published_at)
 values('31000000-0000-0000-0000-000000000001','21000000-0000-0000-0000-000000000001','1.0.0','Sync fixture','Easy','Geometry',repeat('0',64),'test-v1','sha256:'||repeat('0',64),'published',now());
set local role authenticated;
set local request.jwt.claims='{"sub":"11000000-0000-0000-0000-000000000001","role":"authenticated"}';
select is((save_workspace_item('31000000-0000-0000-0000-000000000001','draft','first',0)->>'revision')::int,1,'new draft starts at revision1');
select is((save_workspace_item('31000000-0000-0000-0000-000000000001','draft','second',1)->>'revision')::int,2,'CAS increments revision');
select is(save_workspace_item('31000000-0000-0000-0000-000000000001','draft','stale',1)->>'ok','false','stale revision cannot overwrite');
select is((select code from public.drafts),'second','conflict preserves account text');
select is(save_workspace_item('31000000-0000-0000-0000-000000000001','note','private note',0)->>'ok','true','owner saves a note');
select is(save_workspace_item('31000000-0000-0000-0000-000000000001','bookmark','1',0)->>'ok','true','owner saves bookmark');
select is(save_workspace_item('31000000-0000-0000-0000-000000000001','bookmark','0',1)->>'revision','2','bookmark removal is a revisioned tombstone');
set local request.jwt.claims='{"sub":"11000000-0000-0000-0000-000000000002","role":"authenticated"}';
select is((select count(*)::integer from public.drafts),0,'another account cannot read text');
select is(save_workspace_item('31000000-0000-0000-0000-000000000001','draft','account B',0)->>'revision','1','another account has an independent revision');
set local request.jwt.claims='{"sub":"11000000-0000-0000-0000-000000000001","role":"authenticated"}';
select is((select code from public.drafts),'second','account B did not alter account A');
reset role;
select * from finish();
rollback;
