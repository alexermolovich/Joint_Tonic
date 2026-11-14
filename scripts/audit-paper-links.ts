import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { fileURLToPath } from "node:url";
import { parsePaperFlow } from "../apps/web/src/lib/paper-flow.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = fs.readdirSync(path.join(root, "content/problems")).flatMap(slug => {
  const file = path.join(root, "content/problems", slug, "meta.json");
  return fs.existsSync(file) ? [JSON.parse(fs.readFileSync(file, "utf8")) as {slug:string;title:string}] : [];
});
const slugs = catalog.map(problem => problem.slug);
const walk = (directory: string): string[] => fs.readdirSync(directory, {withFileTypes:true}).flatMap(entry => {
  const full = path.join(directory, entry.name);
  return entry.isDirectory() ? walk(full) : entry.name.endsWith(".md") ? [full] : [];
});
const errors: string[] = [], rows: string[] = [];
const sources = new Set<string>();
let cards = 0, stages = 0, runnable = 0, planned = 0, covered = 0;
const cell = (value: string) => value.replaceAll("|", "\\|").replaceAll("\n", " ");
for (const file of walk(path.join(root, "research/papers"))) {
  const {data, content} = matter(fs.readFileSync(file, "utf8"));
  cards++;
  sources.add(String(data.primary_url).trim().replace(/\/$/, ""));
  const label = path.relative(path.join(root, "research"), file).split(path.sep).join("/");
  try {
    const flow = parsePaperFlow(data.execution_flow, content, slugs, catalog);
    if (!flow) throw Error("Missing execution flow");
    for (const node of flow.nodes) {
      stages++;
      runnable += node.problem_slugs.length;
      planned += node.planned_problems?.length || 0;
      if (node.problem_slugs.length || node.planned_problems?.length) covered++;
      else errors.push(label + "/" + node.id + ": no associated exercise or planned idea");
      const ready = node.problem_slugs.map(slug => "[" + cell(catalog.find(p => p.slug === slug)!.title) + "](http://localhost:3000/problems/" + slug + ")");
      const pending = (node.planned_problems || []).map(title => cell(title));
      rows.push("| [" + cell(String(data.title)) + "](" + label + ") | " + cell(node.title) + " | " + (ready.join("<br>") || "—") + " | " + (pending.join("<br>") || "—") + " |");
    }
  } catch (error) {
    errors.push(label + ": " + (error instanceof Error ? error.message : String(error)));
  }
}
const summary = {cards, distinctPapers:sources.size, stages, coveredStages:covered, runnableAssociations:runnable, plannedAssociations:planned, errors};
console.log(JSON.stringify(summary, null, 2));
if (process.argv.includes("--write")) {
  const report = [
    "# Paper component implementation map", "",
    "Generated from each paper card's execution flow and the published problem catalog. Runnable links refer to the local website. Planned entries are ideas or blueprints, not runnable tasks or claims of full paper reproduction.", "",
    "Cards: " + cards + "; distinct papers: " + sources.size + "; mapped stages: " + covered + "/" + stages + "; runnable stage associations: " + runnable + "; planned stage associations: " + planned + ".", "",
    "Refresh with: node --experimental-strip-types scripts/audit-paper-links.ts --write", "",
    "| Paper | Explained component | Runnable exercises | Planned exercises |",
    "|---|---|---|---|", ...rows, "",
    "## Remaining mapping issues", "", ...(errors.length ? errors.map(error => "- " + error) : ["None detected by the structural audit. Mathematical/source fidelity still requires the independent content review."]), "",
  ].join("\n");
  fs.writeFileSync(path.join(root, "research/FLOW_PROBLEM_MAP.md"), report);
}
if (errors.length) process.exitCode = 1;
