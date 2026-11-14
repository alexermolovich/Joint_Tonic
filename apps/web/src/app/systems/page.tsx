import{Suspense}from"react";import{Catalog}from"@/components/catalog";import{getProblems}from"@/lib/content";
export const metadata={title:"Systems"};export default function Page(){return <Suspense fallback={<main id="main" className="page">Loading systems…</main>}><Catalog systems problems={getProblems()}/></Suspense>}
