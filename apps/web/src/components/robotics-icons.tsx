import type { ReactNode } from "react";

// Original line drawings, shared by the catalog's topic chips and problem rows.
const topics: Record<string, ReactNode> = {
  Geometry: <><path d="M6 18V3m0 15h15M6 18 17 7" /><path d="m3 6 3-3 3 3m9 9 3 3-3 3M13 7h4v4" /><circle className="jt-icon-accent" cx="6" cy="18" r="2.3" fill="currentColor" stroke="none" /></>,
  Perception: <><path d="m6 7 2-3h6l2 3" /><rect x="2.5" y="7" width="16" height="13" rx="2.5" /><circle cx="10.5" cy="13.5" r="3.5" /><path className="jt-icon-accent" d="m21 8 1.5-1m-1.5 6.5h1.5M21 19l1.5 1" /><circle className="jt-icon-accent" cx="10.5" cy="13.5" r="1" fill="currentColor" stroke="none" /></>,
  VLM: <><circle cx="8" cy="13" r="5" /><path d="m11.5 16.5 4 4M13 9V3h9v10h-5l-3 2v-3" /><path className="jt-icon-accent" d="M16 6h3M16 9h3M6 13h4m-2-2v4" /></>,
  VLA: <><rect x="8.5" y="2.5" width="7" height="5" rx="1.5" /><path d="m9 7.5-4 5V19h3.5v-4m6.5-7.5 4 5V19h-3.5v-4M12 3v3" /><path className="jt-icon-accent" d="m12 15 2.5 1.5v3L12 21l-2.5-1.5v-3L12 15Z" /></>,
  "Robot learning": <><path d="M3 21h11M6 21v-4h5v4M7.5 13.7 5 9m2-3 7-2m3 2 3 4-1 3m1-3 2 2" /><circle cx="8.5" cy="15.5" r="2" /><circle cx="5" cy="7" r="2" /><circle cx="16" cy="4.5" r="2" /><path className="jt-icon-accent" d="M15 17a4 4 0 0 1 7 2m0-3v3h-3" /></>,
  MLOps: <><rect x="2" y="9" width="5" height="6" rx="1.3" /><rect x="16" y="3" width="6" height="6" rx="1.3" /><rect x="16" y="15" width="6" height="6" rx="1.3" /><path d="M7 12h5m0 0V7a1 1 0 0 1 1-1h3m-4 6v5a1 1 0 0 0 1 1h3" /><circle className="jt-icon-accent" cx="12" cy="12" r="1.7" fill="currentColor" stroke="none" /><path className="jt-icon-accent" d="m18 18 1 1 1.5-2" /></>,
};

const allTopics = <><rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" /><path className="jt-icon-accent" d="m17.5 2.5 4 4-4 4-4-4 4-4Z" /></>;

export function RoboticsIcon({ topic, size = 20 }: { topic: string; size?: number }) {
  return <svg className="jt-robotics-icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.65" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">{topics[topic] || allTopics}</svg>;
}

export function RuntimeIcon({ framework, size = 18 }: { framework: string; size?: number }) {
  return <svg className="jt-robotics-icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.65" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
    {framework === "NumPy" ? <><path d="M5 3H2v18h3M19 3h3v18h-3" /><rect x="6.5" y="6.5" width="3.5" height="3.5" rx=".5" /><rect x="14" y="6.5" width="3.5" height="3.5" rx=".5" /><rect x="6.5" y="14" width="3.5" height="3.5" rx=".5" /><rect className="jt-icon-accent" x="14" y="14" width="3.5" height="3.5" rx=".5" fill="currentColor" /></> : framework === "PyTorch" ? <><path d="m5.5 5.7 5 2m-5 3.7 5-2.7m-5 4.6 5 2m-5 3 5-2M13.5 8.5l5 2.7m-5 4.3 5-2.7" /><circle cx="4" cy="5" r="1.8" /><circle cx="4" cy="12" r="1.8" /><circle cx="4" cy="19" r="1.8" /><circle cx="12" cy="8" r="1.8" /><circle cx="12" cy="16" r="1.8" /><circle className="jt-icon-accent" cx="20" cy="12" r="2.2" /></> : <><path d="m8 6-5 6 5 6m8-12 5 6-5 6" /><path className="jt-icon-accent" d="m14 4-4 16" /></>}
  </svg>;
}
