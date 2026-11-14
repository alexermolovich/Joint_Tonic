import type { Metadata } from "next";
import { AppShell } from "@/components/app-shell";
import { getPapers, getProblems, getTracks } from "@/lib/content";
import { buildNavigation } from "@/lib/navigation";
import { AuthProvider } from "@/components/auth-provider";
import { ThemeProvider } from "@/components/theme-provider";
import "katex/dist/katex.min.css";
import "./globals.css";
import "@/components/app-shell.css";
export const metadata:Metadata={title:{default:"Joint Tonic — Physical AI, in practice",template:"%s · Joint Tonic"},description:"Learn physical AI by implementing the components behind robotics research. Practical Python problems, visual theory, and reproducible tests."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en" data-scroll-behavior="smooth" data-theme="gruvbox" style={{colorScheme:"dark"}} suppressHydrationWarning><head><script dangerouslySetInnerHTML={{__html:'(function(){try{var t=localStorage.getItem("joint-tonic-theme");if(t==="gruvbox"||t==="slate"||t==="light"||t==="graphite"){document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t==="light"?"light":"dark"}}catch(e){}})()'}}/></head><body><ThemeProvider><AuthProvider problemVersions={Object.fromEntries(getProblems().map(p=>[p.slug,p.version]))}><a href="#main" className="skip-link">Skip to content</a><AppShell navigation={buildNavigation(getProblems(),getPapers(),getTracks())}>{children}</AppShell></AuthProvider></ThemeProvider></body></html>}
