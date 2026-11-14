"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { Braces, ChartNoAxesCombined, ChevronDown, Code2, FolderTree, Home, Menu, PanelLeftClose, PanelLeftOpen, Route, Search, Settings2, Workflow, X, UserRound } from "lucide-react";
import { useAuth } from "./auth-provider";
import type { NavigationItem } from "@/lib/navigation";

const icons = { home: Home, problems: Code2, tracks: Route, projects: FolderTree, systems: Workflow, progress: ChartNoAxesCombined, settings: Settings2, account: UserRound };

function activeBranches(items: NavigationItem[], pathname: string): string[] {
  return items.flatMap(item => {
    const nested = activeBranches(item.children || [], pathname);
    return item.children && (item.href === pathname || nested.length || item.children.some(child => child.href === pathname)) ? [item.id, ...nested] : [];
  });
}

function searchTree(items: NavigationItem[], query: string): NavigationItem[] {
  if (!query) return items;
  return items.flatMap(item => {
    if (`${item.label} ${item.keywords || ""}`.toLowerCase().includes(query)) return [item];
    const children = searchTree(item.children || [], query);
    return children.length ? [{ ...item, children }] : [];
  });
}

export function AppShell({ children, navigation }: { children: ReactNode; navigation: NavigationItem[] }) {
  const pathname = usePathname();
  const { user } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [mobile, setMobile] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState<string[]>(() => activeBranches(navigation, pathname));
  const drawer = useRef<HTMLDialogElement>(null);
  const search = query.trim().toLowerCase();
  const filtered = searchTree(navigation, search);

  useEffect(() => {
    const media = window.matchMedia("(max-width: 760px)");
    const update = () => { setMobile(media.matches); if (!media.matches) drawer.current?.close(); };
    update(); media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    setExpanded(items => [...new Set([...items, ...activeBranches(navigation, pathname)])]);
    setQuery("");
    drawer.current?.close();
  }, [pathname, navigation]);

  function toggle(id: string) {
    setExpanded(items => items.includes(id) ? items.filter(item => item !== id) : [...items, id]);
  }
  function followLink() { drawer.current?.close(); setQuery(""); }
  function tree(items: NavigationItem[], scope: string, compact: boolean, depth = 0): ReactNode {
    return <ul className={depth ? "app-tree-children" : "app-tree"}>{items.map(item => {
      const Icon = item.icon ? icons[item.icon] : null;
      const open = !compact && (Boolean(search) || expanded.includes(item.id));
      const selected = item.href === pathname;
      return <li key={item.id}><div className="app-tree-row" data-active={selected}>
        <Link href={item.href} onClick={followLink} aria-current={selected ? "page" : undefined} aria-label={item.label} title={compact ? item.label : undefined}>
          {Icon && <Icon size={19} aria-hidden="true" />}<span className="app-tree-label">{item.label}</span>{item.count !== undefined && <small className="app-tree-count">{item.count}</small>}
        </Link>
        {!!item.children?.length && !compact && <button type="button" aria-label={`${open ? "Collapse" : "Expand"} ${item.label}`} aria-expanded={open} aria-controls={`${scope}-${item.id}`} disabled={Boolean(search)} onClick={() => toggle(item.id)}><ChevronDown size={15} aria-hidden="true" /></button>}
      </div>{!!item.children?.length && <div id={`${scope}-${item.id}`} hidden={!open}>{tree(item.children, scope, compact, depth + 1)}</div>}</li>;
    })}</ul>;
  }
  function contents(scope: string, compact: boolean) {
    return <>
      {!compact && <label className="app-navigation-search"><Search size={16} aria-hidden="true" /><input aria-label="Search navigation" placeholder="Find a page or paper…" value={query} onChange={event => setQuery(event.target.value)} /></label>}
      <nav className="app-navigation-tree" aria-label="Main navigation">{tree(compact ? navigation : filtered, scope, compact)}{!compact && !filtered.length && <p className="app-navigation-empty" role="status">No matching pages or papers.</p>}</nav>
      <div className="app-navigation-foot"><span className="live-dot" /><Link href="/account" className="app-tree-label" onClick={followLink}>{user ? "Your account" : "Sign in"}</Link></div>
    </>;
  }

  return <div className="app-shell" data-collapsed={collapsed}>
    <aside className="app-sidebar" data-compact={collapsed || mobile} aria-label="Site navigation">
      <div className="app-navigation-brand"><Link href="/" aria-label="Joint Tonic home" onClick={followLink}><span className="app-navigation-logo"><Braces size={23} /></span><span className="app-tree-label">joint<span>tonic</span></span></Link></div>
      <button type="button" className="app-navigation-toggle" aria-label={mobile ? "Open navigation" : collapsed ? "Expand navigation" : "Collapse navigation"} aria-expanded={mobile ? mobileOpen : !collapsed} aria-controls={mobile ? "navigation-drawer" : "desktop-navigation"} onClick={() => { if (mobile) { drawer.current?.showModal(); setMobileOpen(true); } else setCollapsed(!collapsed); }}>
        {mobile ? <Menu size={19} /> : collapsed ? <PanelLeftOpen size={19} /> : <PanelLeftClose size={19} />}<span className="app-tree-label">Collapse sidebar</span>
      </button>
      <div id="desktop-navigation" className="app-navigation-content">{contents("desktop", collapsed || mobile)}</div>
    </aside>
    <div className="app-content">{children}</div>
    <dialog ref={drawer} id="navigation-drawer" className="app-navigation-drawer" aria-label="Site navigation" onClose={() => setMobileOpen(false)} onClick={event => { if (event.target === event.currentTarget) drawer.current?.close(); }}>
      <div className="app-drawer-heading"><strong>Joint Tonic</strong><button className="icon-button" aria-label="Close navigation" onClick={() => drawer.current?.close()}><X size={20} /></button></div>
      {contents("mobile", false)}
    </dialog>
  </div>;
}
