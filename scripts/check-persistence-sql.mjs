import {PGlite} from '../.local/persistence-db-test/node_modules/@electric-sql/pglite/dist/index.js';
import fs from 'node:fs';
const db=new PGlite();
await db.exec(`
create role anon;create role authenticated;create role service_role bypassrls;
create schema auth;create schema extensions;
create table auth.users(id uuid primary key,email text,raw_user_meta_data jsonb);
create function auth.uid() returns uuid language sql stable as $$select (nullif(current_setting('request.jwt.claims',true),'')::jsonb->>'sub')::uuid$$;
grant usage on schema auth to anon,authenticated,service_role;
grant execute on function auth.uid() to anon,authenticated,service_role;
create function public.plan(n integer) returns text language sql as $$select 'plan '||n$$;
create function public.ok(v boolean,label text) returns text language plpgsql as $$begin if v is distinct from true then raise exception 'assertion failed: %',label;end if;return 'ok '||label;end;$$;
create function public.is(actual anyelement,expected anyelement,label text) returns text language plpgsql as $$begin if actual is distinct from expected then raise exception 'assertion failed: % actual=% expected=%',label,actual,expected;end if;return 'ok '||label;end;$$;
create function public.lives_ok(command text,label text) returns text language plpgsql as $$begin execute command;return 'ok '||label;end;$$;
create function public.throws_ok(command text,expected_state text,expected_message text,label text) returns text language plpgsql as $$declare caught text;message text;begin begin execute command;exception when others then get stacked diagnostics caught=returned_sqlstate,message=message_text;end;if caught is distinct from expected_state then raise exception 'assertion failed: % expected SQLSTATE %, got % (%)',label,expected_state,caught,message;end if;if expected_message is not null and message is distinct from expected_message then raise exception 'assertion failed: % wrong message',label;end if;return 'ok '||label;end;$$;
create function public.finish() returns setof text language sql as $$select 'finished'$$;
`);
for(const name of fs.readdirSync('supabase/migrations').filter(n=>n.endsWith('.sql')).sort()){
 await db.exec(fs.readFileSync('supabase/migrations/'+name,'utf8'));console.log('migration applied',name);
}
for(const name of ['platform_rls.test.sql','workspace_sync.test.sql','trusted_evaluation.test.sql']){
 const sql=fs.readFileSync('supabase/tests/database/'+name,'utf8').replace(/create extension if not exists pgtap with schema extensions;/i,'');
 const result=await db.exec(sql);let assertions=0;
 for(const part of result)for(const row of part.rows||[])for(const value of Object.values(row))if(typeof value==='string'&&value.startsWith('ok '))assertions++;
 console.log(name,assertions,'actual PostgreSQL assertions passed (local assertion wrappers, not pgTAP extension)');
}
await db.close();
