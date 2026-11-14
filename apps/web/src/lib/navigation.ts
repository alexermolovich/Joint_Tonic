import type { Paper, ProblemMeta, Track } from "./types";
import { projectSheet, projectSheets } from "./projects";

export type NavigationItem = {
  id: string;
  label: string;
  href: string;
  icon?: "home" | "problems" | "tracks" | "projects" | "systems" | "progress" | "settings" | "account";
  count?: number;
  keywords?: string;
  children?: NavigationItem[];
};

export function buildNavigation(problems: ProblemMeta[], papers: Paper[], tracks: Track[]): NavigationItem[] {
  const problemSlugs = new Set(problems.map(problem => problem.slug));
  const capstones = problems.filter(problem => problem.slug.startsWith("capstone-")).map(problem => ({ id: `capstone-${problem.slug}`, label: problem.title, href: `/projects/capstones/${problem.slug.slice("capstone-".length)}` }));
  const topics = projectSheets.map(sheet => {
    const children = papers.filter(paper => projectSheet(paper.category)?.slug === sheet.slug).map(paper => ({
      id: `paper-${paper.id}`, label: paper.title, href: `/projects/${paper.id}`, keywords: `${paper.id} ${paper.topics.join(" ")}`,
    }));
    return {
      id: `topic-${sheet.slug}`, label: sheet.title, href: `/projects/sheets/${sheet.slug}`,
      count: children.length, children,
    };
  });

  return [
    { id: "home", label: "Home", href: "/", icon: "home" },
    {
      id: "problems", label: "Problems", href: "/problems", icon: "problems", count: problems.length,
      children: problems.map(problem => ({ id: `problem-${problem.slug}`, label: problem.title, href: `/problems/${problem.slug}` })),
    },
    {
      id: "tracks", label: "Tracks", href: "/tracks", icon: "tracks", count: tracks.length,
      children: [...tracks.filter(track => !track.slug.startsWith("paper-")).map(track => ({
        id: `track-${track.slug}`, label: track.title, href: `/tracks/${track.slug}`,
        count: new Set(track.slugs.filter(slug => problemSlugs.has(slug))).size,
      })), ...projectSheets.map(sheet => {
        const children = tracks.filter(track => track.slug.startsWith("paper-") && papers.some(paper => `paper-${paper.id}` === track.slug && projectSheet(paper.category)?.slug === sheet.slug)).map(track => ({ id: `track-${track.slug}`, label: track.title, href: `/tracks/${track.slug}`, count: track.slugs.length }));
        return { id: `track-topic-${sheet.slug}`, label: sheet.title, href: `/tracks?topic=${sheet.slug}`, count: children.length, children };
      }).filter(topic => topic.children.length)],
    },
    { id: "projects", label: "Projects", href: "/projects", icon: "projects", count: papers.length + capstones.length, children: [{ id: "capstones", label: "Capstone projects", href: "/projects/capstones", count: capstones.length, children: capstones }, ...topics] },
    { id: "systems", label: "Systems", href: "/systems", icon: "systems" },
    { id: "progress", label: "Progress", href: "/progress", icon: "progress" },
    { id: "account", label: "Account", href: "/account", icon: "account", keywords: "login sign in register profile" },
    { id: "settings", label: "Settings", href: "/settings", icon: "settings" },
  ];
}
