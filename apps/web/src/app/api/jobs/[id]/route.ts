import { NextRequest, NextResponse } from "next/server";
import { backendConnection, WorkspaceAuthError } from "@/lib/backend-connection";
export async function GET(request:NextRequest,{params}:{params:Promise<{id:string}>}){
  const{id}=await params;if(!/^[a-f0-9-]{36}$/.test(id))return NextResponse.json({error:"Invalid job"},{status:400});
  try{const connection=await backendConnection(request,"worker");const response=await fetch(new URL(`/jobs/${id}`,connection.endpoint),{headers:connection.headers,cache:"no-store",signal:AbortSignal.timeout(5000)});return NextResponse.json(await response.json(),{status:response.status,headers:{"Cache-Control":"no-store"}});}
  catch(error){if(error instanceof WorkspaceAuthError)return NextResponse.json({error:error.message},{status:error.status});return NextResponse.json({error:"Runner connection interrupted. Retry shortly."},{status:503});}
}
