-- Joint Tonic local persistence baseline.
-- Learner code, hidden tests and reference implementations never execute in SQL.
begin;

create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create function private.touch_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.created_at := old.created_at;
  new.updated_at := clock_timestamp();
  return new;
end;
$$;

create function private.reject_record_update()
returns trigger language plpgsql set search_path = '' as $$
begin
  raise exception 'record is immutable; create a new version or evaluation'
    using errcode = '55000';
end;
$$;

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null default '' check (char_length(display_name) <= 80),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create function private.create_user_profile()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, left(coalesce(new.raw_user_meta_data ->> 'display_name', ''), 80));
  return new;
end;
$$;
create trigger on_auth_user_created after insert on auth.users
for each row execute function private.create_user_profile();

create table public.problems (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.problem_versions (
  id uuid primary key default gen_random_uuid(),
  problem_id uuid not null references public.problems(id) on delete restrict,
  version text not null check (version ~ '^[0-9]+\.[0-9]+\.[0-9]+$'),
  title text not null check (char_length(title) between 1 and 200),
  difficulty text not null check (difficulty in ('Easy', 'Medium', 'Hard', 'Research')),
  domain text not null,
  topics text[] not null default '{}',
  paper_ids text[] not null default '{}',
  metadata jsonb not null default '{}' check (
    jsonb_typeof(metadata) = 'object' and octet_length(metadata::text) <= 65536),
  content_sha256 text not null check (content_sha256 ~ '^[a-f0-9]{64}$'),
  evaluator_version text not null check (char_length(evaluator_version) > 0),
  runtime_image_digest text check (runtime_image_digest ~ '^sha256:[a-f0-9]{64}$'),
  state text not null default 'draft' check (state in ('draft', 'published', 'retired')),
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (problem_id, version),
  check ((state = 'draft' and published_at is null)
      or (state in ('published', 'retired') and published_at is not null)),
  check (published_at is null or runtime_image_digest is not null)
);
create index problem_versions_catalog on public.problem_versions (state, domain, difficulty);
create index problem_versions_topics on public.problem_versions using gin (topics);

create function private.protect_published_version()
returns trigger language plpgsql set search_path = '' as $$
begin
  if old.published_at is not null and
     ((to_jsonb(new) - 'state' - 'updated_at') is distinct from
      (to_jsonb(old) - 'state' - 'updated_at')) then
    raise exception 'published content is immutable; create a new semantic version'
      using errcode = '55000';
  end if;
  if old.published_at is not null and new.state = 'draft' then
    raise exception 'a published version cannot return to draft' using errcode = '55000';
  end if;
  return new;
end;
$$;
create trigger protect_problem_version before update on public.problem_versions
for each row execute function private.protect_published_version();

create table public.drafts (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  problem_version_id uuid not null references public.problem_versions(id) on delete restrict,
  code text not null default '' check (octet_length(code) <= 100000),
  language text not null default 'python' check (language = 'python'),
  revision bigint not null default 1 check (revision > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, problem_version_id)
);
create table public.notes (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  problem_version_id uuid not null references public.problem_versions(id) on delete restrict,
  body text not null default '' check (octet_length(body) <= 100000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, problem_version_id)
);
create index drafts_problem_version on public.drafts (problem_version_id);
create index notes_problem_version on public.notes (problem_version_id);

create table public.jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  problem_version_id uuid not null references public.problem_versions(id) on delete restrict,
  mode text not null check (mode in ('run', 'submit')),
  status text not null default 'queued'
    check (status in ('queued', 'running', 'completed', 'failed', 'cancelled')),
  code text not null check (octet_length(code) between 1 and 100000),
  correlation_id uuid not null default gen_random_uuid(),
  idempotency_key text check (char_length(idempotency_key) between 1 and 128),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  started_at timestamptz,
  finished_at timestamptz,
  -- Only bounded, learner-safe result summaries belong here; never hidden inputs.
  result jsonb check (
    jsonb_typeof(result) = 'object' and octet_length(result::text) <= 262144),
  error text check (octet_length(error) <= 8192),
  unique (user_id, id, problem_version_id),
  check ((status = 'queued' and started_at is null and finished_at is null
                              and result is null and error is null)
      or (status = 'running' and started_at is not null and finished_at is null
                               and result is null and error is null)
      or (status in ('completed', 'failed', 'cancelled') and finished_at is not null)),
  check (finished_at is null or finished_at >= created_at),
  check (started_at is null or started_at >= created_at),
  check (finished_at is null or started_at is null or finished_at >= started_at)
);
create unique index jobs_idempotency on public.jobs (user_id, idempotency_key)
where idempotency_key is not null;
create index jobs_user_history on public.jobs (user_id, created_at desc);
create index jobs_claim_queue on public.jobs (created_at, id) where status = 'queued';
create index jobs_problem_version on public.jobs (problem_version_id);

create function private.protect_job_transition()
returns trigger language plpgsql set search_path = '' as $$
begin
  if (new.id, new.user_id, new.problem_version_id, new.mode, new.code,
      new.correlation_id, new.idempotency_key, new.created_at)
      is distinct from
     (old.id, old.user_id, old.problem_version_id, old.mode, old.code,
      old.correlation_id, old.idempotency_key, old.created_at) then
    raise exception 'job identity and submitted source are immutable' using errcode = '55000';
  end if;
  if not ((old.status = 'queued' and new.status in ('running', 'cancelled'))
       or (old.status = 'running' and new.status in ('completed', 'failed', 'cancelled'))) then
    raise exception 'invalid or terminal job transition' using errcode = '55000';
  end if;
  if old.started_at is not null and new.started_at is distinct from old.started_at then
    raise exception 'job start time is immutable' using errcode = '55000';
  end if;
  return new;
end;
$$;
create trigger protect_job before update on public.jobs
for each row execute function private.protect_job_transition();

create table public.submissions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  problem_version_id uuid not null references public.problem_versions(id) on delete restrict,
  job_id uuid not null unique,
  created_at timestamptz not null default now(),
  unique (user_id, id, problem_version_id),
  foreign key (user_id, job_id, problem_version_id)
    references public.jobs(user_id, id, problem_version_id) on delete cascade
);
create index submissions_user_history on public.submissions (user_id, created_at desc);
create index submissions_problem_version on public.submissions (problem_version_id);

create function private.check_submission_job()
returns trigger language plpgsql set search_path = '' as $$
begin
  if not exists (
    select 1 from public.jobs
    where id = new.job_id and user_id = new.user_id
      and problem_version_id = new.problem_version_id and mode = 'submit'
  ) then
    raise exception 'submission must reference its owner and a submit job'
      using errcode = '23514';
  end if;
  return new;
end;
$$;
create trigger check_submission_job before insert on public.submissions
for each row execute function private.check_submission_job();
create trigger immutable_submission before update on public.submissions
for each row execute function private.reject_record_update();

create table public.evaluations (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique references public.submissions(id) on delete cascade,
  verdict text not null check (verdict in ('passed', 'failed', 'error')),
  evaluator_version text not null check (char_length(evaluator_version) > 0),
  runtime_image_digest text not null check (runtime_image_digest ~ '^sha256:[a-f0-9]{64}$'),
  fixture_sha256 text not null check (fixture_sha256 ~ '^[a-f0-9]{64}$'),
  seed bigint not null,
  duration_ms numeric not null check (duration_ms >= 0),
  passed_count integer not null check (passed_count >= 0),
  total_count integer not null check (total_count >= passed_count),
  summary jsonb not null default '{}' check (
    jsonb_typeof(summary) = 'object' and octet_length(summary::text) <= 262144),
  correlation_id uuid not null,
  created_at timestamptz not null default now(),
  check (verdict <> 'passed' or (passed_count = total_count and total_count > 0))
);
create index evaluations_created on public.evaluations (created_at desc);
create trigger immutable_evaluation before update on public.evaluations
for each row execute function private.reject_record_update();

create table public.progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  problem_version_id uuid not null references public.problem_versions(id) on delete restrict,
  solved_at timestamptz not null,
  -- First verified passing submission, set only by the trusted control plane.
  submission_id uuid not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, problem_version_id),
  foreign key (user_id, submission_id, problem_version_id)
    references public.submissions(user_id, id, problem_version_id) on delete cascade
);
create index progress_submission on public.progress (submission_id);
create index progress_problem_version on public.progress (problem_version_id);

create function private.check_verified_progress()
returns trigger language plpgsql set search_path = '' as $$
begin
  if not exists (
    select 1 from public.evaluations
    where submission_id = new.submission_id and verdict = 'passed'
  ) then
    raise exception 'solved progress requires a passing evaluation' using errcode = '23514';
  end if;
  return new;
end;
$$;
create trigger verified_progress before insert or update on public.progress
for each row execute function private.check_verified_progress();

create table public.bookmarks (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  problem_id uuid not null references public.problems(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, problem_id)
);
create index bookmarks_problem on public.bookmarks (problem_id);

-- RLS is enabled explicitly on every API-visible application table.
alter table public.profiles enable row level security;
alter table public.problems enable row level security;
alter table public.problem_versions enable row level security;
alter table public.drafts enable row level security;
alter table public.notes enable row level security;
alter table public.jobs enable row level security;
alter table public.submissions enable row level security;
alter table public.evaluations enable row level security;
alter table public.progress enable row level security;
alter table public.bookmarks enable row level security;

-- Replace Supabase's broad table defaults with explicit application privileges.
revoke all on public.profiles, public.problems, public.problem_versions,
  public.drafts, public.notes, public.jobs, public.submissions, public.evaluations,
  public.progress, public.bookmarks from anon, authenticated;
grant select on public.problems, public.problem_versions to anon, authenticated;
grant select, insert, update on public.profiles to authenticated;
grant select, insert, update, delete on public.drafts, public.notes, public.bookmarks to authenticated;
grant select, insert on public.jobs to authenticated;
grant select on public.submissions, public.evaluations, public.progress to authenticated;
grant all on public.profiles, public.problems, public.problem_versions,
  public.drafts, public.notes, public.jobs, public.submissions, public.evaluations,
  public.progress, public.bookmarks to service_role;

create policy read_published_problem on public.problems for select to anon, authenticated
using (exists (select 1 from public.problem_versions v
               where v.problem_id = problems.id and v.published_at is not null));
create policy read_published_version on public.problem_versions for select to anon, authenticated
using (published_at is not null);

create policy read_own_profile on public.profiles for select to authenticated
using ((select auth.uid()) = id);
create policy insert_own_profile on public.profiles for insert to authenticated
with check ((select auth.uid()) = id);
create policy update_own_profile on public.profiles for update to authenticated
using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create policy own_drafts on public.drafts for all to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id and exists (
  select 1 from public.problem_versions v
  where v.id = problem_version_id and v.published_at is not null));
create policy own_notes on public.notes for all to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id and exists (
  select 1 from public.problem_versions v
  where v.id = problem_version_id and v.published_at is not null));
create policy own_bookmarks on public.bookmarks for all to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id and exists (
  select 1 from public.problem_versions v
  where v.problem_id = bookmarks.problem_id and v.published_at is not null));

create policy read_own_jobs on public.jobs for select to authenticated
using ((select auth.uid()) = user_id);
create policy enqueue_own_job on public.jobs for insert to authenticated
with check ((select auth.uid()) = user_id and status = 'queued'
  and started_at is null and finished_at is null and result is null and error is null
  and exists (select 1 from public.problem_versions v
              where v.id = problem_version_id and v.published_at is not null));
create policy read_own_submissions on public.submissions for select to authenticated
using ((select auth.uid()) = user_id);
create policy read_own_evaluations on public.evaluations for select to authenticated
using (exists (select 1 from public.submissions s
               where s.id = submission_id and s.user_id = (select auth.uid())));
create policy read_own_progress on public.progress for select to authenticated
using ((select auth.uid()) = user_id);

-- Service/controller writes to jobs, evaluations and verified progress are deliberate.
-- No service-role secret is ever passed to learner workloads or browser code.
create trigger profiles_updated before update on public.profiles
for each row execute function private.touch_updated_at();
create trigger problems_updated before update on public.problems
for each row execute function private.touch_updated_at();
create trigger versions_updated before update on public.problem_versions
for each row execute function private.touch_updated_at();
create trigger drafts_updated before update on public.drafts
for each row execute function private.touch_updated_at();
create trigger notes_updated before update on public.notes
for each row execute function private.touch_updated_at();
create trigger jobs_updated before update on public.jobs
for each row execute function private.touch_updated_at();
create trigger progress_updated before update on public.progress
for each row execute function private.touch_updated_at();

-- Prevent future direct RPC invocation of trigger helpers in the private schema.
revoke all on all functions in schema private from public, anon, authenticated;

comment on table public.evaluations is
  'Append-only evaluator evidence; contains safe summaries, never hidden test inputs.';
comment on table public.progress is
  'Verified solves only. Browser-local completion flags are not imported as trusted scores.';
comment on column public.problem_versions.metadata is
  'Public catalog metadata only. Do not place reference solutions, hidden tests, or secrets here.';
comment on table public.jobs is
  'Bounded snapshots and lifecycle metadata. A separate isolated worker executes the source.';

commit;
