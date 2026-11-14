-- Account drafts/notes need immutable content identities before a worker is hosted.
-- A catalog-only version is explicitly unavailable for trusted execution.
begin;

do $$
declare
  matching_constraints text[];
begin
  select array_agg(conname::text) into matching_constraints
  from pg_catalog.pg_constraint
  where conrelid = 'public.problem_versions'::regclass and contype = 'c'
    and regexp_replace(lower(pg_catalog.pg_get_constraintdef(oid)), '[[:space:]()]', '', 'g')
      = 'checkpublished_atisnullorruntime_image_digestisnotnull';
  if coalesce(cardinality(matching_constraints), 0) <> 1 then
    raise exception 'expected exactly one original publication/runtime constraint';
  end if;
  execute format('alter table public.problem_versions drop constraint %I', matching_constraints[1]);
end;
$$;

alter table public.problem_versions
  add constraint problem_versions_publication_runtime check (
    published_at is null
    or runtime_image_digest is not null
    or (runtime_image_digest is null
        and coalesce(metadata ->> 'grading_protocol' = 'unavailable', false))
  );

comment on column public.problem_versions.runtime_image_digest is
  'Actual immutable OCI digest when assigned. NULL on a published version requires explicit grading_protocol=unavailable; never substitute a placeholder.';

-- record_evaluation already requires a real digest and data-only-functions-v1,
-- and compares both against this immutable row. Catalog-only rows fail those
-- checks, even for the trusted service-role caller. Existing RLS is unchanged.
-- Qualifying execution later requires a new content version; this migration does
-- not permit updating the identity of an already published catalog version.
commit;
