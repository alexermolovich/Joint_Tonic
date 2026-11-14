"use client";

import { CheckCircle2 } from "lucide-react";
import { type ThemeId, useTheme } from "./theme-provider";
import "./theme-settings.css";

const themes: { id: ThemeId; name: string; description: string }[] = [
  { id: "gruvbox", name: "Gruvbox Dark", description: "Warm charcoal, cream text, and orange." },
  { id: "slate", name: "Slate Dark", description: "Cool gray, clear white text, and amber." },
  { id: "light", name: "Warm Light", description: "Soft paper, dark text, and burnt orange." },
  { id: "graphite", name: "Graphite", description: "Neutral charcoal, clear white text, and mint." },
];

export function ThemeSettings() {
  const { theme, setTheme } = useTheme();
  return (
    <section className="settings-card theme-settings" aria-labelledby="appearance-heading">
      <h2 id="appearance-heading">Appearance</h2>
      <p>Choose a theme for the website, theory reader, and code editor. Changes apply immediately and are saved in this browser when storage is available.</p>
      <div className="theme-options" role="group" aria-label="Color theme">
        {themes.map(option => (
          <button
            key={option.id}
            type="button"
            className="theme-option"
            aria-pressed={theme === option.id}
            aria-label={option.name}
            onClick={() => setTheme(option.id)}
          >
            <span className={`theme-preview theme-preview-${option.id}`} aria-hidden="true">
              <span className="theme-preview-nav"><i /><i /><i /></span>
              <span className="theme-preview-content"><span>Aa</span><i /><i /><i /></span>
            </span>
            <span className="theme-option-title">{option.name}<CheckCircle2 size={18} aria-hidden="true" /></span>
            <span className="theme-option-description">{option.description}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
