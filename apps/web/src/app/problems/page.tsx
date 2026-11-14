import {Suspense}from"react";import{Catalog}from"@/components/catalog";import{getProblems,tracks}from"@/lib/content";
export const metadata={title:"Problems"};export default function Page(){return <Suspense fallback={<main id="main" className="page">Loading problems…</main>}><Catalog problems={getProblems()} tracks={tracks}/></Suspense>}
