import { NextRequest, NextResponse } from "next/server";
const worker=process.env.WORKER_URL||"http://127.0.0.1:8765";
export async function POST(request:NextRequest){
  const origin=request.headers.get("origin");
  if(origin && new URL(origin).host!==request.headers.get("host")) return NextResponse.json({error:"Cross-origin request rejected"},{status:403});
  try{const body=await request.text(); if(body.length>100000)return NextResponse.json({error:"Source is too large"},{status:413});
    const response=await fetch(`${worker}/jobs`,{method:"POST",headers:{"Content-Type":"application/json","X-Workspace-Id":request.headers.get("x-workspace-id")||""},body,signal:AbortSignal.timeout(5000)});
    return NextResponse.json(await response.json(),{status:response.status});
  }catch{return NextResponse.json({error:"The isolated runner is offline. Start the app with npm run dev to launch the WSL worker."},{status:503});}
}
