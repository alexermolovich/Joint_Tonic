-- Run with: npm exec supabase -- test db
-- Every fixture is rolled back, including Auth users.
begin;
create extension if not exists pgtap with schema extensions;
set local search_path = public, extensions;
select plan(18);

insert into auth.users (id, email, raw_user_meta_data) values
  ('10000000-0000-0000-0000-000000000001', 'a@joint-tonic.test', '{}'),
  ('10000000-0000-0000-0000-000000000002', 'b@joint-tonic.test', '{}');
insert into public.problems (id, slug)
values ('20000000-0000-0000-0000-000000000001', 'rls-fixture');
insert into public.problem_versions (
  id, problem_id, version, title, difficulty, domain,
  content_sha256, evaluator_version, runtime_image_digest, state, published_at
) values (
  '30000000-0000-0000-0000-000000000001',
  '20000000-0000-0000-0000-000000000001', '1.0.0', 'RLS fixture', 'Easy', 'Geometry',
  repeat('0', 64), 'test-v1', 'sha256:' || repeat('0', 64), 'published', now()
);

set local role authenticated;
set local request.jwt.claims = '{"sub":"10000000-0000-0000-0000-000000000001","role":"authenticated"}';
select is((select count(*)::integer from public.profiles), 1, 'profile reads are owner-scoped');
select is((select count(*)::integer from public.problems), 1, 'published catalog is visible');
select lives_ok($test$
  insert into public.drafts (problem_version_id, code)
  values ('30000000-0000-0000-0000-000000000001', 'print(1)')
$test$, 'owner can insert a draft with auth.uid default');
select is((select count(*)::integer from public.drafts), 1, 'owner sees the draft');
select throws_ok($test$
  insert into public.drafts (user_id, problem_version_id, code)
  values ('10000000-0000-0000-0000-000000000002',
          '30000000-0000-0000-0000-000000000001', 'forged')
$test$, '42501', null, 'owner cannot insert another user draft');
select throws_ok($test$
  insert into public.jobs (problem_version_id, mode, status, code, finished_at)
  values ('30000000-0000-0000-0000-000000000001', 'submit', 'completed', 'forged', now())
$test$, '42501', null, 'browser cannot forge a completed job');
select lives_ok($test$
  insert into public.jobs (id, problem_version_id, mode, code)
  values ('40000000-0000-0000-0000-000000000001',
          '30000000-0000-0000-0000-000000000001', 'submit', 'return 1')
$test$, 'owner can enqueue a queued snapshot');
select throws_ok($test$
  insert into public.progress (user_id, problem_version_id, solved_at, submission_id)
  values ('10000000-0000-0000-0000-000000000001',
          '30000000-0000-0000-0000-000000000001', now(),
          '50000000-0000-0000-0000-000000000001')
$test$, '42501', null, 'browser cannot forge verified progress');

set local request.jwt.claims = '{"sub":"10000000-0000-0000-0000-000000000002","role":"authenticated"}';
select is((select count(*)::integer from public.drafts), 0, 'another user cannot read draft code');
select is((select count(*)::integer from public.jobs), 0, 'another user cannot read job code');
select is((select count(*)::integer from public.profiles), 1, 'another user sees only their profile');

reset role;
update public.jobs set status = 'running', started_at = clock_timestamp()
where id = '40000000-0000-0000-0000-000000000001';
update public.jobs set status = 'completed', finished_at = clock_timestamp(), result = '{"passed":true}'
where id = '40000000-0000-0000-0000-000000000001';
select throws_ok($test$
  update public.jobs set result = '{"passed":false}'
  where id = '40000000-0000-0000-0000-000000000001'
$test$, '55000', null, 'terminal job result is immutable');

insert into public.submissions (id, user_id, problem_version_id, job_id) values (
  '50000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001',
  '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001');
select throws_ok($test$
  update public.submissions set created_at = now()
  where id = '50000000-0000-0000-0000-000000000001'
$test$, '55000', null, 'submitted evidence cannot be updated');

insert into public.evaluations (
  submission_id, verdict, evaluator_version, runtime_image_digest, fixture_sha256,
  seed, duration_ms, passed_count, total_count, correlation_id
) values (
  '50000000-0000-0000-0000-000000000001', 'passed', 'test-v1',
  'sha256:' || repeat('0', 64), repeat('1', 64), 7, 1, 3, 3,
  '60000000-0000-0000-0000-000000000001');
select throws_ok($test$
  update public.evaluations set verdict = 'failed'
  where submission_id = '50000000-0000-0000-0000-000000000001'
$test$, '55000', null, 'evaluation evidence cannot be updated');
select lives_ok($test$
  insert into public.progress (user_id, problem_version_id, solved_at, submission_id)
  values ('10000000-0000-0000-0000-000000000001',
          '30000000-0000-0000-0000-000000000001', now(),
          '50000000-0000-0000-0000-000000000001')
$test$, 'trusted controller can persist a verified solve');

insert into public.jobs (id, user_id, problem_version_id, mode, code)
values ('40000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000002',
        '30000000-0000-0000-0000-000000000001', 'submit', 'return 0');
insert into public.submissions (id, user_id, problem_version_id, job_id)
values ('50000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000002',
        '30000000-0000-0000-0000-000000000001',
        '40000000-0000-0000-0000-000000000002');
select throws_ok($test$
  insert into public.progress (user_id, problem_version_id, solved_at, submission_id)
  values ('10000000-0000-0000-0000-000000000002',
          '30000000-0000-0000-0000-000000000001', now(),
          '50000000-0000-0000-0000-000000000002')
$test$, '23514', null, 'a submission without a passing evaluation cannot establish progress');

set local role authenticated;
set local request.jwt.claims = '{"sub":"10000000-0000-0000-0000-000000000002","role":"authenticated"}';
select is((select count(*)::integer from public.evaluations), 0, 'evaluation reads honor submission owner');
set local request.jwt.claims = '{"sub":"10000000-0000-0000-0000-000000000001","role":"authenticated"}';
select is((select count(*)::integer from public.evaluations), 1, 'owner can inspect immutable evaluation');

reset role;
select * from finish();
rollback;
