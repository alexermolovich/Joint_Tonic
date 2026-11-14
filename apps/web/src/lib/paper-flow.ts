import type { PaperFlow, PaperFlowNode } from "./types";

export function paperSectionId(title: string) {
  return `paper-section-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`;
}

// A malformed diagram must not publish broken stage/problem links.
export function parsePaperFlow(value: unknown, markdown: string, problemSlugs: string[], catalog: { slug: string; title: string }[] = []): PaperFlow | undefined {
  if (value === undefined) return undefined;
  const object = (item: unknown): Record<string, unknown> => {
    if (!item || typeof item !== "object" || Array.isArray(item)) throw new Error("Expected flow object");
    return item as Record<string, unknown>;
  };
  const text = (item: unknown, max = 300): string => {
    if (typeof item !== "string" || !item.trim() || item.length > max) throw new Error("Invalid flow text");
    return item.trim();
  };
  const position = (item: unknown, limit: number): number => {
    if (typeof item !== "number" || !Number.isInteger(item) || item < 0 || item > limit) throw new Error("Invalid flow position");
    return item;
  };
  const flow = object(value);
  if (!Array.isArray(flow.nodes) || flow.nodes.length < 2 || flow.nodes.length > 24 || !Array.isArray(flow.edges) || flow.edges.length > 48) throw new Error("Invalid flow size");
  const headings = new Set([...markdown.matchAll(/^#{2,3}\s+(.+)\r?$/gm)].map(match => match[1].trim()));
  const ids = new Set<string>();
  const positions = new Set<string>();
  const normalizeTitle = (title: string) => title.trim().toLowerCase().replace(/\s+/g, " ");
  const nodes: PaperFlowNode[] = flow.nodes.map(item => {
    const node = object(item);
    const id = text(node.id, 60);
    const column = position(node.column, 7);
    const row = position(node.row, 11);
    const section = text(node.section, 150);
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id) || ids.has(id) || positions.has(`${column},${row}`)) throw new Error("Duplicate or invalid flow node");
    if (!headings.has(section)) throw new Error(`Missing flow section: ${section}`);
    const slugs = node.problem_slugs ?? [];
    if (!Array.isArray(slugs) || slugs.some(slug => typeof slug !== "string" || !problemSlugs.includes(slug))) throw new Error("Unknown flow problem");
    const ideas = node.planned_problems ?? [];
    if (!Array.isArray(ideas) || ideas.length > 12) throw new Error("Invalid planned problems");
    const planned: string[] = [];
    const runnable = [...slugs] as string[];
    for (const idea of [...new Set(ideas.map(item => text(item, 200)))]) {
      const matches = catalog.filter(problem => problemSlugs.includes(problem.slug) && normalizeTitle(problem.title) === normalizeTitle(idea));
      // Promote only an unambiguous exact title, never a guessed keyword match.
      if (matches.length === 1) runnable.push(matches[0].slug);
      else planned.push(idea);
    }
    ids.add(id); positions.add(`${column},${row}`);
    return { id, title: text(node.title, 100), detail: text(node.detail), column, row, section, problem_slugs: [...new Set(runnable)], ...(node.planned_problems !== undefined ? { planned_problems: planned } : {}) };
  });
  const edges = flow.edges.map(item => {
    const edge = object(item);
    const from = text(edge.from, 60); const to = text(edge.to, 60);
    if (!ids.has(from) || !ids.has(to) || from === to) throw new Error("Invalid flow edge");
    return { from, to, label: text(edge.label, 80) };
  });
  return { title: text(flow.title, 150), description: text(flow.description, 600), nodes, edges };
}
