/**
 * Monaco Editor: локальная сборка (без CDN) + тёмная тема для workbench-а.
 * Импортируется как side-effect из компонентов редактора.
 */
import { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor";
import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";

// Для Python-подсветки достаточно editor worker (токенизация синхронная).
self.MonacoEnvironment = {
  getWorker(_: unknown, _label: string) {
    return new editorWorker();
  },
};

// Используем локальный билд Monaco вместо загрузки с CDN.
loader.config({ monaco });

// Тёмная тема в стиле LeetCode / среды.
monaco.editor.defineTheme("yx-dark", {
  base: "vs-dark",
  inherit: true,
  rules: [
    { token: "comment", foreground: "7c8aa5", fontStyle: "italic" },
    { token: "keyword", foreground: "c084fc" },
    { token: "string", foreground: "6ee7b7" },
    { token: "number", foreground: "fbbf24" },
    { token: "delimiter", foreground: "94a3b8" },
    { token: "type", foreground: "60a5fa" },
    { token: "identifier", foreground: "e2e8f0" },
    { token: "function", foreground: "38bdf8" },
  ],
  colors: {
    "editor.background": "#0b1220",
    "editor.foreground": "#e2e8f0",
    "editor.lineHighlightBackground": "#111a2c",
    "editorLineNumber.foreground": "#334155",
    "editorLineNumber.activeForeground": "#e2e8f0",
    "editorCursor.foreground": "#fbbf24",
    "editor.selectionBackground": "#1e3a5f80",
    "editor.inactiveSelectionBackground": "#1e3a5f40",
    "editorIndentGuide.background1": "#1e293b",
    "editorWidget.background": "#0f172a",
    "editorWidget.border": "#1e293b",
    "scrollbarSlider.background": "#33415566",
    "scrollbarSlider.hoverBackground": "#47556966",
    "scrollbarSlider.activeBackground": "#64748b66",
  },
});

export default monaco;