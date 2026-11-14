import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { Children, isValidElement, type ReactNode } from "react";
import { paperSectionId } from "@/lib/paper-flow";
function headingText(children: ReactNode): string {
  return Children.toArray(children).map(child => typeof child === "string" || typeof child === "number" ? String(child) : isValidElement<{children?: ReactNode}>(child) ? headingText(child.props.children) : "").join("");
}
export function Markdown({children,paperAnchors=false}:{children:string;paperAnchors?:boolean}) {
  return <div className="prose"><ReactMarkdown remarkPlugins={[remarkGfm,remarkMath]} rehypePlugins={[rehypeKatex]} components={{a:({children,href})=><a href={href} target={href?.startsWith("http")?"_blank":undefined} rel="noreferrer">{children}</a>,h2:({children})=><h2 id={paperAnchors?paperSectionId(headingText(children)):undefined}>{children}</h2>,h3:({children})=><h3 id={paperAnchors?paperSectionId(headingText(children)):undefined}>{children}</h3>}}>{children}</ReactMarkdown></div>;
}
