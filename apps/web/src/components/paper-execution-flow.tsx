import Link from "next/link";
import { ArrowDownRight, ArrowRight, FileCode2 } from "lucide-react";
import type { PaperFlow, ProblemMeta } from "@/lib/types";
import { paperSectionId } from "@/lib/paper-flow";
import "./paper-execution-flow.css";

const nodeWidth = 210, nodeHeight = 164, columnStep = 254, rowStep = 230, padding = 24;

export function PaperExecutionFlow({ flow, paperId, problems }: { flow: PaperFlow; paperId: string; problems: ProblemMeta[] }) {
  const width = (Math.max(...flow.nodes.map(node => node.column)) * columnStep) + nodeWidth + padding * 2;
  const height = (Math.max(...flow.nodes.map(node => node.row)) * rowStep) + nodeHeight + padding * 2;
  const position = (id: string) => {
    const node = flow.nodes.find(item => item.id === id)!;
    return { x: padding + node.column * columnStep, y: padding + node.row * rowStep };
  };
  const marker = `flow-arrow-${paperId}`;
  const exercisesId = (nodeId: string) => `paper-exercises-${paperId}-${nodeId}`;
  return <section className="paper-execution" aria-labelledby="execution-heading">
    <div className="paper-execution-heading"><div><span className="eyebrow">FROM PAPER TO COMPONENTS</span><h2 id="execution-heading">{flow.title}</h2></div><p>{flow.description}</p></div>
    <div className="paper-execution-layout">
      <nav aria-label="Paper implementation stages" className="paper-stage-list"><ol>
        {flow.nodes.map((node, index) => <li key={node.id} id={exercisesId(node.id)}>
          <a className="paper-stage-link" href={`#${paperSectionId(node.section)}`}><span className="paper-stage-number">{index + 1}</span><span><strong>{node.title}</strong><small>{node.detail}</small></span><ArrowDownRight size={17} aria-hidden="true" /></a>
          {node.problem_slugs.length > 0 && <div className="paper-stage-problems">{node.problem_slugs.map(slug => {
            const problem = problems.find(item => item.slug === slug);
            return problem && <Link key={slug} href={`/problems/${slug}`}><FileCode2 size={15} aria-hidden="true" /><span>{problem.title}<small>{problem.difficulty} · {problem.framework} · Runnable</small></span><ArrowRight size={14} aria-hidden="true" /></Link>;
          })}</div>}
          {!!node.planned_problems?.length && <div className="paper-stage-planned" aria-label="Planned exercises"><span className="paper-planned-label">Planned exercises</span>{node.planned_problems.map(title => <p key={title}><strong>{title}</strong><small>Implementation pending · not yet runnable</small></p>)}</div>}
        </li>)}
      </ol></nav>
      <div className="paper-flow-panel"><div className="paper-flow-caption"><strong>Model execution flow</strong><span>Select a stage for its math. Implement opens a runnable exercise; planned exercises show the remaining components.</span></div>
        <div className="paper-flow-scroll" tabIndex={0} role="region" aria-label="Scrollable model execution graph">
          <div className="paper-flow-canvas" style={{ width, height }}>
            <svg width={width} height={height} aria-hidden="true"><defs><marker id={marker} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--muted)" /></marker></defs>
              {flow.edges.map((edge, index) => {
                const from = position(edge.from), to = position(edge.to);
                const vertical = from.x === to.x;
                const downward = to.y > from.y;
                const crossRow = from.y !== to.y;
                const x1 = vertical ? from.x + nodeWidth / 2 : from.x + nodeWidth;
                const y1 = vertical ? from.y + (downward ? nodeHeight : 0) : from.y + nodeHeight / 2;
                const x2 = vertical ? to.x + nodeWidth / 2 : to.x;
                const y2 = vertical ? to.y + (downward ? 0 : nodeHeight) : to.y + nodeHeight / 2;
                const midX = (x1 + x2) / 2, midY = (y1 + y2) / 2;
                const path = vertical ? `M${x1},${y1} L${x2},${y2}` : `M${x1},${y1} H${midX} V${y2} H${x2}`;
                return <g key={`${edge.from}-${edge.to}-${index}`}><path d={path} fill="none" stroke="var(--muted)" strokeWidth="1.5" markerEnd={`url(#${marker})`} /><text x={vertical || crossRow ? midX + 9 : midX} y={vertical || crossRow ? midY + 4 : from.y - 8} textAnchor={vertical || crossRow ? "start" : "middle"}>{edge.label}</text></g>;
              })}
            </svg>
            {flow.nodes.map((node, index) => {
              const plannedCount = node.planned_problems?.length || 0;
              const singleProblem = node.problem_slugs.length === 1 ? problems.find(problem => problem.slug === node.problem_slugs[0]) : undefined;
              return <div key={node.id} className={`paper-flow-node${node.problem_slugs.length ? " has-problem" : ""}`} style={{ left: padding + node.column * columnStep, top: padding + node.row * rowStep, width: nodeWidth, height: nodeHeight }}>
                <a className="paper-flow-node-summary" href={`#${paperSectionId(node.section)}`}><span>STAGE {String(index + 1).padStart(2, "0")}</span><strong>{node.title}</strong><small>{node.problem_slugs.length} runnable{plannedCount ? ` · ${plannedCount} planned` : ""}</small></a>
                {singleProblem ? <Link className="paper-flow-practice" href={`/problems/${singleProblem.slug}`} aria-label={`Implement ${singleProblem.title}`} title={singleProblem.title}><FileCode2 size={14} aria-hidden="true" />Implement<ArrowRight size={13} aria-hidden="true" /></Link>
                  : node.problem_slugs.length + plannedCount > 0 ? <a className="paper-flow-practice" href={`#${exercisesId(node.id)}`}><FileCode2 size={14} aria-hidden="true" />{node.problem_slugs.length ? "View exercises" : "View planned exercises"}<ArrowDownRight size={13} aria-hidden="true" /></a> : null}
              </div>;
            })}
          </div>
        </div>
        <details className="paper-flow-text"><summary>Read the flow as text</summary><ul>{flow.edges.map((edge, index) => <li key={index}><strong>{flow.nodes.find(node => node.id === edge.from)?.title}</strong> → {flow.nodes.find(node => node.id === edge.to)?.title}<span>{edge.label}</span></li>)}</ul></details>
      </div>
    </div>
  </section>;
}
