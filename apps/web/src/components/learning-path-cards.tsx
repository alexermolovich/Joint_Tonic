"use client";

import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import type { ProblemMeta, Track } from "@/lib/types";
import { useWorkspace } from "@/lib/local-workspace";
import "./learning-path-cards.css";

export function LearningPathCards({ tracks, problems }: { tracks: Track[]; problems: ProblemMeta[] }) {
  const { state } = useWorkspace();
  if (!tracks.length) return null;

  return <section className="jt-learning-paths" aria-labelledby="jt-learning-paths-title">
    <div className="jt-learning-paths-heading">
      <h2 id="jt-learning-paths-title">Learning paths</h2>
      <Link href="/tracks">View all paths <ArrowRight size={14} aria-hidden="true" /></Link>
    </div>
    <ul className="jt-learning-path-list">
      {tracks.map(track => {
        const trackProblems = problems.filter(problem => track.slugs.includes(problem.slug));
        const solved = trackProblems.filter(problem => state.solved.includes(problem.slug)).length;
        const levels = (["Easy", "Medium", "Hard"] as const).map(name => ({
          name, count: trackProblems.filter(problem => problem.difficulty === name).length,
        })).filter(level => level.count > 0);
        return <li key={track.slug}>
        <Link href={`/tracks/${track.slug}`} className="jt-learning-path-card">
          <span className="jt-learning-path-stats">
            <span className="jt-learning-path-solved"><strong>{solved} / {trackProblems.length}</strong> solved</span>
            <span className="jt-learning-path-levels" aria-label="Problem difficulty counts">
              {levels.map(level => <span key={level.name} className={`jt-path-difficulty ${level.name.toLowerCase()}`}>{level.count} {level.name}</span>)}
            </span>
          </span>
          <span className={`jt-learning-path-body${track.slug === "vision-to-action" ? " has-art" : ""}`}>
            {track.slug === "vision-to-action" && <Image
              className="jt-learning-path-image"
              src="/images/learning-paths/manipulation.png"
              alt="Robot arm holding an orange cube"
              width={128}
              height={128}
              sizes="(max-width: 1100px) 88px, 96px"
            />}
            <span className="jt-learning-path-copy">
              <span className="jt-learning-path-topic">{track.subtitle}</span>
              <strong>{track.title}</strong>
              <span className="jt-learning-path-count">Guided path <ArrowUpRight size={13} aria-hidden="true" /></span>
            </span>
          </span>
        </Link>
      </li>;
      })}
    </ul>
  </section>;
}
