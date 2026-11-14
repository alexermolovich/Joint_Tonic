import type { Metadata } from "next";
import { Nav } from "@/components/nav";
import "katex/dist/katex.min.css";
import "./globals.css";
export const metadata:Metadata={title:{default:"Joint Tonic — Physical AI, in practice",template:"%s · Joint Tonic"},description:"Learn physical AI by implementing the components behind robotics research. Ten practical Python problems, visual theory, and reproducible tests."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><a href="#main" className="skip-link">Skip to content</a><Nav/>{children}<footer className="site-footer"><span>jointtonic <span className="muted">/ From research to the real world.</span></span><div><a href="/papers">Paper library</a><a href="/settings">Settings</a><span className="local-indicator"><i/> Local workspace</span></div></footer></body></html>}
