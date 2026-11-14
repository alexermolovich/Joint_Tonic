import { NextRequest, NextResponse } from "next/server";
export async function GET(request:NextRequest,{params}:{params:Promise<{id:string}>}){
  const{id}=await params;if(!/^[a-f0-9-]{36}$/.test(id))return NextResponse.json({error:"Invalid job"},{status:400});
  try{const response=await fetch(`${process.env.WORKER_URL||"http://127.0.0.1:8765"}/jobs/${id}`,{headers:{"X-Workspace-Id":request.headers.get("x-workspace-id")||""},cache:"no-store",signal:AbortSignal.timeout(5000)});return NextResponse.json(await response.json(),{status:response.status});}
  catch{return NextResponse.json({error:"Runner connection interrupted. Retry shortly."},{status:503});}
}
