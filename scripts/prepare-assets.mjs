import fs from 'node:fs';
const source='node_modules/monaco-editor/min/vs';const target='apps/web/public/monaco/vs';
if(!fs.existsSync(target)&&fs.existsSync(source)){fs.mkdirSync('apps/web/public/monaco',{recursive:true});fs.cpSync(source,target,{recursive:true});}
