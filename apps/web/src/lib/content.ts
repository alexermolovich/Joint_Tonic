import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { cache } from "react";
import type { Problem, ProblemMeta, Paper, Track } from "./types";

export function repoRoot() {
  let dir = process.cwd();
  for (let i=0;i<5;i++) { if (fs.existsSync(path.join(dir,"SPEC.md"))) return dir; dir=path.dirname(dir); }
  throw new Error("Cannot locate Joint Tonic repository");
}
const read = (file: string) => fs.readFileSync(file,"utf8");
export const getProblems = cache((): ProblemMeta[] => {
  const dir=path.join(repoRoot(),"content/problems");
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(slug=>fs.existsSync(path.join(dir,slug,"meta.json"))).map(slug=>JSON.parse(read(path.join(dir,slug,"meta.json"))) as ProblemMeta).sort((a,b)=>a.number-b.number);
});
export const getProblem = cache((slug: string): Problem | null => {
  const meta=getProblems().find(p=>p.slug===slug); if(!meta) return null;
  const dir=path.join(repoRoot(),"content/problems",meta.slug);
  return {...meta, problem:read(path.join(dir,"problem.md")), theory:read(path.join(dir,"theory.md")), starter:read(path.join(dir,"starter.py")), solution:read(path.join(dir,"solution.md")), reference:read(path.join(dir,"reference.py"))};
});
export const getPapers = cache((): Paper[] => {
  const base=path.join(repoRoot(),"research/papers"); const papers:Paper[]=[]; const seen=new Set<string>();
  if (!fs.existsSync(base)) return papers;
  const walk=(dir:string)=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})) {
      const file=path.join(dir,entry.name); if(entry.isDirectory()) {walk(file);continue;}
      if(!entry.name.endsWith(".md")) continue;
      try {
        const {data,content}=matter(read(file)); if(!data.title||!data.primary_url) continue;
        const canonical=String(data.primary_url).replace(/\/?$/," ").trim(); if(seen.has(canonical)) continue; seen.add(canonical);
        const id=entry.name.slice(0,-3);
        const brief=(content.split(/## Agent brief\s*/i)[1]||content).split(/\n## /)[0].replace(/^#+ .*$/gm,"").trim();
        papers.push({id,title:String(data.title),year:Number(data.year),authors:Array.isArray(data.authors)?data.authors:[String(data.authors)],topics:Array.isArray(data.topics)?data.topics:[],primaryUrl:String(data.primary_url),category:path.basename(dir),brief,content,problemSlugs:getProblems().filter(p=>p.paperIds?.includes(id)).map(p=>p.slug)});
      } catch { /* A concurrent research download may not have published its card yet. */ }
    }
  };walk(base);return papers.sort((a,b)=>b.year-a.year||a.title.localeCompare(b.title));
});
export const tracks:Track[]=[
  {slug:"robot-perception-foundations",title:"From coordinates to detections",subtitle:"GEOMETRY & PERCEPTION",description:"Build the five components between a camera observation and a clean detection set. Follow a point through coordinate frames, projection, overlap, decoding, and suppression.",icon:"scan",color:"green",slugs:["se3-transform-points","project-camera-points","box-iou-broadcast","decode-yolo-grid","class-aware-nms"],objectives:["Move points between explicit camera and world frames","Project geometry with valid depth and image bounds","Compose IoU, a YOLO-style decoder, and class-aware NMS","Inspect deterministic edge cases and failure modes"]},
  {slug:"vision-to-action",title:"Connect vision to robot actions",subtitle:"VLM & ROBOT LEARNING",description:"Implement the small mechanisms behind multimodal alignment, discrete robot actions, and diffusion training. Study original paper components with bounded CPU fixtures.",icon:"brain",color:"blue",slugs:["clip-symmetric-loss","rt1-action-codec","diffusion-action-noising"],objectives:["Align paired image and text embeddings","Represent bounded continuous actions as tokens","Construct reproducible diffusion training targets"]},
  {slug:"robot-mlops",title:"Ship with evidence",subtitle:"ROBOTICS MLOPS",description:"Turn raw multimodal episodes into validated training inputs, then decide whether a model meets a measured release contract.",icon:"workflow",color:"orange",slugs:["validate-robot-episodes","edge-inference-release-gate"],objectives:["Locate sensor, schema, and timestamp anomalies","Evaluate quality and latency by hardware class","Produce deterministic evidence for a release decision"]}
];
