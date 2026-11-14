import {spawn} from 'node:child_process';
import path from 'node:path';
import {cpSync, mkdirSync} from 'node:fs';
const root = process.cwd();
const monacoSource = path.join(root, 'node_modules/monaco-editor/min/vs');
const monacoTarget = path.join(root, 'apps/web/public/monaco/vs');
mkdirSync(path.dirname(monacoTarget), {recursive:true});
cpSync(monacoSource, monacoTarget, {recursive:true, force:true});
const wslRoot = root.replaceAll('\\','/').replace(/^([A-Za-z]):/,(_,drive)=>'/mnt/'+drive.toLowerCase());
const worker = process.platform === 'win32'
  ? spawn('wsl.exe',['--cd',wslRoot,'--exec','/home/alex/.venvs/joint-tonic/bin/python','-u','apps/worker/server.py'],{stdio:'inherit',windowsHide:true})
  : spawn(process.env.JOINT_TONIC_PYTHON || 'python3',['-u','apps/worker/server.py'],{stdio:'inherit'});
const simulator = process.platform === 'win32'
  ? spawn('wsl.exe',['--cd',wslRoot,'--exec','/home/alex/.venvs/joint-tonic/bin/python','-u','apps/simulator/server.py'],{stdio:'inherit',windowsHide:true})
  : spawn(process.env.JOINT_TONIC_PYTHON || 'python3',['-u','apps/simulator/server.py'],{stdio:'inherit'});
simulator.on('error', () => console.warn('MuJoCo simulator did not start. See docs/mujoco-fr3.md; coding remains available.'));
simulator.on('exit', code => { if (code) console.warn('MuJoCo simulator stopped. See docs/mujoco-fr3.md; coding remains available.'); });
const web = spawn(process.execPath,[path.join(root,'node_modules/next/dist/bin/next'),'dev','apps/web','--hostname','127.0.0.1'],{stdio:'inherit',windowsHide:true});
function stop(){worker.kill();simulator.kill();web.kill();}
process.on('SIGINT',()=>{stop();process.exit(0)});
process.on('SIGTERM',()=>{stop();process.exit(0)});
web.on('exit',code=>{stop();process.exit(code||0)});
