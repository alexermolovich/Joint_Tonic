-- Account workspace synchronization. Scores remain read-only to learners.
begin;
alter table public.notes add column revision bigint not null default 1 check (revision between 1 and 9007199254740991);
alter table public.bookmarks add column revision bigint not null default 1 check (revision between 1 and 9007199254740991);
alter table public.bookmarks add column bookmarked boolean not null default true;
alter table public.drafts add constraint drafts_safe_revision check (revision <= 9007199254740991);

create function private.bump_workspace_revision()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.revision := old.revision + 1;
  return new;
end;
$$;
create trigger bump_draft_revision before update on public.drafts for each row execute function private.bump_workspace_revision();
create trigger bump_note_revision before update on public.notes for each row execute function private.bump_workspace_revision();
create trigger bump_bookmark_revision before update on public.bookmarks for each row execute function private.bump_workspace_revision();

-- SECURITY INVOKER preserves the existing owner-only RLS. No user_id parameter.
-- Empty bodies / false bookmarks are tombstones: stale devices cannot resurrect deletes.
create function public.save_workspace_item(p_problem_version_id uuid, p_kind text, p_body text, p_expected_revision bigint)
returns jsonb language plpgsql security invoker set search_path = '' as $$
declare
  owner_id uuid := auth.uid();
  problem_id_value uuid;
  current_body text;
  current_revision bigint;
  inserted integer;
begin
  if owner_id is null then raise exception 'authentication required' using errcode = '42501'; end if;
  if p_kind is null or p_kind not in ('draft','note','bookmark') or p_body is null or octet_length(p_body)>100000
     or p_expected_revision is null or p_expected_revision<0 or p_expected_revision>9007199254740991
     or (p_kind='bookmark' and p_body not in ('0','1')) then
    raise exception 'invalid workspace item' using errcode='22023';
  end if;
  select v.problem_id into problem_id_value from public.problem_versions v
    where v.id=p_problem_version_id and v.published_at is not null;
  if problem_id_value is null then raise exception 'published version required' using errcode='22023'; end if;

  if p_kind='draft' then
    if p_expected_revision=0 then
      insert into public.drafts(user_id,problem_version_id,code) values(owner_id,p_problem_version_id,p_body) on conflict do nothing;
      get diagnostics inserted = row_count;
      if inserted=1 then return jsonb_build_object('ok',true,'revision',1,'body',p_body); end if;
    end if;
    select d.code,d.revision into current_body,current_revision from public.drafts d
      where d.user_id=owner_id and d.problem_version_id=p_problem_version_id for update;
    if current_revision is distinct from p_expected_revision then
      return jsonb_build_object('ok',false,'revision',coalesce(current_revision,0),'body',coalesce(current_body,''));
    end if;
    update public.drafts set code=p_body where user_id=owner_id and problem_version_id=p_problem_version_id returning revision into current_revision;
  elsif p_kind='note' then
    if p_expected_revision=0 then
      insert into public.notes(user_id,problem_version_id,body) values(owner_id,p_problem_version_id,p_body) on conflict do nothing;
      get diagnostics inserted = row_count;
      if inserted=1 then return jsonb_build_object('ok',true,'revision',1,'body',p_body); end if;
    end if;
    select n.body,n.revision into current_body,current_revision from public.notes n
      where n.user_id=owner_id and n.problem_version_id=p_problem_version_id for update;
    if current_revision is distinct from p_expected_revision then
      return jsonb_build_object('ok',false,'revision',coalesce(current_revision,0),'body',coalesce(current_body,''));
    end if;
    update public.notes set body=p_body where user_id=owner_id and problem_version_id=p_problem_version_id returning revision into current_revision;
  else
    if p_expected_revision=0 then
      insert into public.bookmarks(user_id,problem_id,bookmarked) values(owner_id,problem_id_value,p_body='1') on conflict do nothing;
      get diagnostics inserted = row_count;
      if inserted=1 then return jsonb_build_object('ok',true,'revision',1,'body',p_body); end if;
    end if;
    select case when b.bookmarked then '1' else '0' end,b.revision into current_body,current_revision from public.bookmarks b
      where b.user_id=owner_id and b.problem_id=problem_id_value for update;
    if current_revision is distinct from p_expected_revision then
      return jsonb_build_object('ok',false,'revision',coalesce(current_revision,0),'body',coalesce(current_body,'0'));
    end if;
    update public.bookmarks set bookmarked=(p_body='1') where user_id=owner_id and problem_id=problem_id_value returning revision into current_revision;
  end if;
  return jsonb_build_object('ok',true,'revision',current_revision,'body',p_body);
end;
$$;
revoke all on function public.save_workspace_item(uuid,text,text,bigint) from public, anon;
grant execute on function public.save_workspace_item(uuid,text,text,bigint) to authenticated;
revoke delete on public.drafts, public.notes, public.bookmarks from authenticated;
comment on function public.save_workspace_item(uuid,text,text,bigint) is 'Owner-scoped compare-and-swap for editable text and bookmark tombstones. Never accepts submissions or grading.';
commit;
