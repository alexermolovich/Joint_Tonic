"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowUpRight, Menu, X, Braces, ChevronDown } from "lucide-react";
import { useState } from "react";
export function Nav(){
 const path=usePathname();const[open,setOpen]=useState(false);
 const links=[["/problems","Problems"],["/tracks","Tracks"],["/papers","Research papers"],["/systems","Systems"]];
 return <><div className="announcement"><span className="live-dot"/> BUILT FOR THE PHYSICAL WORLD <span className="announcement-sep">/</span> Ten practical problems. One place to start. <Link href="/problems">Explore the collection <ArrowUpRight size={12}/></Link></div><header className="site-header"><div className="nav-inner"><Link href="/" className="brand" aria-label="Joint Tonic home"><span className="brand-mark"><Braces size={23}/></span>joint<span className="brand-light">tonic</span><span className="beta">BETA</span></Link><nav aria-label="Main navigation" className={open?"nav-links open":"nav-links"}>{links.map(([href,label])=><Link key={href} href={href} onClick={()=>setOpen(false)} className={path.startsWith(href)?"active":""}>{label}</Link>)}</nav><Link className="nav-progress" href="/progress">My workspace <ChevronDown size={13}/></Link><button className="mobile-menu icon-button" aria-label={open?"Close navigation":"Open navigation"} onClick={()=>setOpen(!open)}>{open?<X/>:<Menu/>}</button></div></header></>;
}
