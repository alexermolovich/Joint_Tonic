"use client";
import {useEffect,useState} from "react";
import type {Job} from "./types";
export type WorkspaceState={id:string;name:string;drafts:Record<string,string>;notes:Record<string,string>;solved:string[];submissions:Job[];activeJobs:Record<string,string>;bookmarks:string[]};
const key="joint-tonic.workspace.v1";
const empty:WorkspaceState={id:"",name:"",drafts:{},notes:{},solved:[],submissions:[],activeJobs:{},bookmarks:[]};
export function readWorkspace():WorkspaceState{if(typeof window==="undefined")return empty;try{return {...empty,...JSON.parse(localStorage.getItem(key)||"{}")}}catch{return empty}}
export function updateWorkspace(fn:(state:WorkspaceState)=>WorkspaceState){const current=readWorkspace();if(!current.id)current.id=crypto.randomUUID();const next=fn(current);localStorage.setItem(key,JSON.stringify(next));window.dispatchEvent(new Event("jt-workspace"));return next;}
export function useWorkspace(){const[state,setState]=useState<WorkspaceState>(empty);const[ready,setReady]=useState(false);useEffect(()=>{if(!readWorkspace().id)updateWorkspace(s=>s);const read=()=>setState(readWorkspace());read();setReady(true);window.addEventListener("jt-workspace",read);window.addEventListener("storage",read);return()=>{window.removeEventListener("jt-workspace",read);window.removeEventListener("storage",read)}},[]);return{state,ready,update:updateWorkspace}}
