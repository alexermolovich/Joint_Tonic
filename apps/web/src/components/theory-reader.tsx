"use client";

import type { Problem } from "@/lib/types";
import { Markdown } from "./markdown";
import { VisualExplorer } from "./visual-explorer";
import "./theory-reader.css";

export function TheoryReader({ problem }: { problem: Problem }) {
  const hasInteractiveVisual = ["transform", "projection", "iou", "yolo", "nms", "clip", "codec", "diffusion", "schema", "benchmark"].includes(problem.visualization);
  const heading = problem.theory.match(/^# ([^\r\n]+)\r?\n/);
  const body = heading ? problem.theory.slice(heading[0].length) : problem.theory;
  // Keep the original explanation intact, with its visual in the article flow.
  const visualSection = body.search(/^## Visual[^\r\n]*$/m);
  const introEnd = visualSection >= 0 ? visualSection : body.search(/\r?\n## (?!Intuition)/);
  const introduction = introEnd >= 0 ? body.slice(0, introEnd) : body;
  const continuation = introEnd >= 0 ? body.slice(introEnd) : "";

  return <article className="inline-theory" aria-label="Theory explanation">
    <Markdown>{introduction}</Markdown>
    {hasInteractiveVisual && <section className="inline-theory-visual" aria-label="Interactive theory lesson">
      <VisualExplorer kind={problem.visualization} />
    </section>}
    <Markdown>{continuation}</Markdown>
  </article>;
}
