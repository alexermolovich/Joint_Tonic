"use client";

import { createContext, useCallback, useContext, useLayoutEffect, useState } from "react";

export type ThemeId = "gruvbox" | "slate" | "light" | "graphite";
type ThemeContextValue = { theme: ThemeId; setTheme: (theme: ThemeId) => void };
const ThemeContext = createContext<ThemeContextValue | null>(null);
const STORAGE_KEY = "joint-tonic-theme";

function isTheme(value: string | null): value is ThemeId {
  return value === "gruvbox" || value === "slate" || value === "light" || value === "graphite";
}

function applyTheme(theme: ThemeId) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme === "light" ? "light" : "dark";
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setCurrentTheme] = useState<ThemeId>("gruvbox");

  useLayoutEffect(() => {
    let saved: ThemeId = "gruvbox";
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      if (isTheme(value)) saved = value;
    } catch {
      // Themes remain usable when this browser blocks local storage.
    }
    applyTheme(saved);
    setCurrentTheme(saved);
  }, []);

  const setTheme = useCallback((next: ThemeId) => {
    applyTheme(next);
    setCurrentTheme(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Keep the selected theme for this session even if it cannot be saved.
    }
  }, []);

  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error("useTheme must be used inside ThemeProvider");
  return value;
}
