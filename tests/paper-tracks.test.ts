import test from "node:test";
import assert from "node:assert/strict";
import {buildPaperTracks} from "../apps/web/src/lib/paper-tracks.ts";
import type {Paper,ProblemMeta} from "../apps/web/src/lib/types.ts";

const paper={id:"2024-example",title:"Example model",year:2024,category:"vla-embodied",brief:"Example",executionFlow:{nodes:[{title:"Encode",problem_slugs:["encode","missing"],planned_problems:["Train adapter"]},{title:"Act",problem_slugs:["encode","act"],planned_problems:["Train adapter","Evaluate policy"]}]}} as Paper;
const problems=[{slug:"encode",title:"Encode",prerequisites:["geometry"]},{slug:"act",title:"Act",prerequisites:["encode"]},{slug:"geometry",title:"Geometry",prerequisites:[]}] as ProblemMeta[];
test("paper tracks retain execution order, deduplicate and separate prerequisites from planned steps",()=>{
 const [track]=buildPaperTracks([paper],problems);
 assert.equal(track.slug,"paper-2024-example");
 assert.deepEqual(track.slugs,["encode","act"]);
 assert.deepEqual(track.plannedTitles,["Train adapter","Evaluate policy"]);
 assert.deepEqual(track.prerequisiteSlugs,["geometry"]);
 assert.deepEqual(track.objectives,["Encode","Act"]);
});
test("a paper without runnable exercises remains a plan with no invented progress",()=>{
 const [track]=buildPaperTracks([{...paper,executionFlow:undefined}],problems);
 assert.deepEqual(track.slugs,[]);assert.deepEqual(track.prerequisiteSlugs,[]);
 assert.equal(track.description,"Example");
 assert.deepEqual(buildPaperTracks([],problems),[]);
});
