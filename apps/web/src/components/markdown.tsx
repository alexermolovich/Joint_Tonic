import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
export function Markdown({children}:{children:string}) {
  return <div className="prose"><ReactMarkdown remarkPlugins={[remarkGfm,remarkMath]} rehypePlugins={[rehypeKatex]} components={{a:({children,href})=><a href={href} target={href?.startsWith("http")?"_blank":undefined} rel="noreferrer">{children}</a>}}>{children}</ReactMarkdown></div>;
}
