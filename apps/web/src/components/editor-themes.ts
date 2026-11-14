import type { BeforeMount } from "@monaco-editor/react";

// Match the site's appearance without remounting the editor or changing its draft.
export const registerEditorThemes: BeforeMount = (monaco) => {
  const palettes = {
    gruvbox: { light: false, background: "#282828", text: "#ebdbb2", muted: "#bdae93", accent: "#fe8019", string: "#b8bb26", number: "#d8a2c1", panel: "#32302f", line: "#504945", selection: "#66512f" },
    slate: { light: false, background: "#1a2430", text: "#e2e8f0", muted: "#afbed0", accent: "#ffb373", string: "#a5d6a1", number: "#c4b2ed", panel: "#22303e", line: "#435268", selection: "#425572" },
    light: { light: true, background: "#fffdf7", text: "#3c3836", muted: "#655c50", accent: "#9c460e", string: "#486119", number: "#79507d", panel: "#efe8d9", line: "#c5b9a4", selection: "#e5cb9c" },
    graphite: { light: false, background: "#191919", text: "#e8e8e8", muted: "#aaaaaa", accent: "#34d399", string: "#8dd5a0", number: "#c9a7e8", panel: "#232323", line: "#424242", selection: "#214e3d" },
  };
  for (const [name, p] of Object.entries(palettes)) {
    monaco.editor.defineTheme(`joint-tonic-${name}`, {
      base: p.light ? "vs" : "vs-dark", inherit: true,
      rules: [
        { token: "comment", foreground: p.muted.slice(1) },
        { token: "keyword", foreground: p.accent.slice(1) },
        { token: "string", foreground: p.string.slice(1) },
        { token: "number", foreground: p.number.slice(1) },
      ],
      colors: {
        "editor.background": p.background, "editor.foreground": p.text,
        "editorLineNumber.foreground": p.muted, "editorLineNumber.activeForeground": p.accent,
        "editorCursor.foreground": p.accent, "editor.selectionBackground": p.selection,
        "editor.inactiveSelectionBackground": p.selection, "editorGutter.background": p.background,
        "editorWidget.background": p.panel, "editorWidget.border": p.line,
        "editorSuggestWidget.background": p.panel, "editorSuggestWidget.border": p.line,
        "editorSuggestWidget.selectedBackground": p.selection,
        "scrollbarSlider.background": `${p.muted}55`, "scrollbarSlider.hoverBackground": `${p.muted}88`,
      },
    });
  }
};
