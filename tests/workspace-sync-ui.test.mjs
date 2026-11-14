import test from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';

const owner='11111111-1111-4111-8111-111111111111';
const user={id:owner,email:'sync@example.test',user_metadata:{display_name:'Sync learner'},app_metadata:{},aud:'authenticated',role:'authenticated',created_at:'2026-01-01T00:00:00Z'};
const token=[{alg:'HS256'},{sub:owner,exp:Math.floor(Date.now()/1000)+3600},'test'].map(v=>Buffer.from(JSON.stringify(v)).toString('base64url')).join('.');

test('account sync keeps guest notes separate, propagates edits and preserves conflicts', {timeout:120000}, async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try {
  const page=await browser.newPage(); const errors=[];page.on('pageerror',e=>errors.push(e.message));
  let body='account note';let revision=1;let patches=0;let offline=false;let currentUser=user;let currentToken=token;
  await page.addInitScript(()=>localStorage.setItem('joint-tonic.workspace.v1',JSON.stringify({id:'22222222-2222-4222-8222-222222222222',notes:{'project-camera-points':'guest note'},drafts:{},solved:[],submissions:[],activeJobs:{},bookmarks:[]})));
  await page.route('**/auth/v1/**',async route=>{
   const path=new URL(route.request().url()).pathname;
   if(path.endsWith('/token'))return route.fulfill({json:{user:currentUser,access_token:currentToken,refresh_token:'test-refresh',expires_in:3600,token_type:'bearer'}});
   if(path.endsWith('/user'))return route.fulfill({json:currentUser});
   if(path.endsWith('/logout'))return route.fulfill({status:204});
   return route.fulfill({status:400,json:{msg:'unexpected auth request'}});
  });
  await page.route('**/api/workspace',async route=>{
   assert.equal(route.request().headers().authorization,`Bearer ${currentToken}`);
   if(offline)return route.fulfill({status:503,json:{error:'offline'}});
   if(route.request().method()==='PATCH'){
    patches++;const change=route.request().postDataJSON();assert.equal(change.kind,'note');assert.equal(change.slug,'project-camera-points');
    if(change.expectedRevision!==revision)return route.fulfill({status:409,json:{ok:false,kind:'note',slug:change.slug,version:'1.0.0',body,revision}});
    body=change.body;revision++;return route.fulfill({json:{ok:true,kind:'note',slug:change.slug,version:'1.0.0',body,revision}});
   }
   return route.fulfill({json:{ownerId:currentUser.id,versions:{'project-camera-points':'1.0.0'},items:[{kind:'note',slug:'project-camera-points',version:'1.0.0',body,revision}],solved:[],submissions:[],activeJobs:{}}});
  });
  await page.goto('http://localhost:3000/account');
  await page.getByLabel('Email',{exact:true}).fill(user.email);await page.getByLabel('Password',{exact:true}).fill('test-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.getByRole('heading',{name:'Your account',exact:true}).waitFor();
  await page.goto('http://localhost:3000/problems/project-camera-points');
  await page.getByText('Saved to your account',{exact:true}).waitFor();
  await page.getByRole('tab',{name:'Notes',exact:true}).click();
  const notes=page.getByRole('textbox',{name:'Private problem notes'});
  await notes.waitFor();await page.waitForFunction(()=>document.querySelector('.notes-editor')?.value==='account note');
  await notes.fill('saved from first device');
  await page.waitForFunction(()=>document.body.textContent.includes('Saved to your account'));
  await page.waitForTimeout(1300);assert.equal(body,'saved from first device');assert.ok(patches>=1);
  body='edited from second device';revision++;
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  await page.waitForFunction(()=>document.querySelector('.notes-editor')?.value==='edited from second device');
  offline=true;await notes.fill('offline local version');await page.waitForTimeout(1400);
  body='conflicting remote version';revision++;offline=false;
  await page.evaluate(()=>window.dispatchEvent(new Event('online')));
  await page.getByText('Edits need review',{exact:false}).waitFor();
  assert.equal(await notes.inputValue(),'offline local version');
  await page.goto('http://localhost:3000/settings');await page.getByRole('button',{name:'Use account version',exact:true}).click();
  await page.goto('http://localhost:3000/account');await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.getByRole('heading',{name:'Welcome back'}).waitFor();
  await page.goto('http://localhost:3000/problems/project-camera-points');await page.getByText('Saved on this device',{exact:true}).waitFor();await page.getByRole('tab',{name:'Notes',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.notes-editor')?.value==='guest note');
  currentUser={...user,id:'33333333-3333-4333-8333-333333333333',email:'second@example.test'};
  currentToken=[{alg:'HS256'},{sub:currentUser.id,exp:Math.floor(Date.now()/1000)+3600},'test'].map(v=>Buffer.from(JSON.stringify(v)).toString('base64url')).join('.');
  body='second account private note';revision=1;
  await page.goto('http://localhost:3000/account');await page.getByLabel('Email',{exact:true}).fill(currentUser.email);await page.getByLabel('Password',{exact:true}).fill('test-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();
  await page.getByRole('heading',{name:'Your account',exact:true}).waitFor();
  await page.goto('http://localhost:3000/problems/project-camera-points');await page.getByText('Saved to your account',{exact:true}).waitFor();await page.getByRole('tab',{name:'Notes',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.notes-editor')?.value==='second account private note');
  const firstAccount=await page.evaluate(id=>JSON.parse(localStorage.getItem('joint-tonic.workspace.v2.account.'+id)),owner);
  assert.equal(firstAccount.notes['project-camera-points'],'conflicting remote version');
  assert.deepEqual(errors,[]);
 } finally {await browser.close();}
});
