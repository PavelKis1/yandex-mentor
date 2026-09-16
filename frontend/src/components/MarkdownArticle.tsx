import { useMemo, useState, type ReactNode, isValidElement } from "react";
import Markdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import oneLight from "react-syntax-highlighter/dist/esm/styles/prism/one-light";
import python from "react-syntax-highlighter/dist/esm/languages/prism/python";
import javascript from "react-syntax-highlighter/dist/esm/languages/prism/javascript";
import typescript from "react-syntax-highlighter/dist/esm/languages/prism/typescript";
import bash from "react-syntax-highlighter/dist/esm/languages/prism/bash";
import sql from "react-syntax-highlighter/dist/esm/languages/prism/sql";
import json from "react-syntax-highlighter/dist/esm/languages/prism/json";
import cpp from "react-syntax-highlighter/dist/esm/languages/prism/cpp";
import java from "react-syntax-highlighter/dist/esm/languages/prism/java";
import go from "react-syntax-highlighter/dist/esm/languages/prism/go";
import yaml from "react-syntax-highlighter/dist/esm/languages/prism/yaml";
import { Check, Copy } from "lucide-react";
import { Callout, type CalloutType } from "./Callout";
import { TabPanel, Tabs } from "./Tabs";
import { CalloutBlock } from "./lecture/CalloutBlock";
import { QuizBlock } from "./lecture/QuizBlock";
import type { QuizOption, QuizQuestion } from "../types";

// Регистрируем поддерживаемые языки для подсветки синтаксиса (ключи refractor'а).
SyntaxHighlighter.registerLanguage("python", python);
SyntaxHighlighter.registerLanguage("javascript", javascript);
SyntaxHighlighter.registerLanguage("typescript", typescript);
SyntaxHighlighter.registerLanguage("bash", bash);
SyntaxHighlighter.registerLanguage("sql", sql);
SyntaxHighlighter.registerLanguage("json", json);
SyntaxHighlighter.registerLanguage("cpp", cpp);
SyntaxHighlighter.registerLanguage("java", java);
SyntaxHighlighter.registerLanguage("go", go);
SyntaxHighlighter.registerLanguage("yaml", yaml);

/** Распространённые алиасы языков в markdown → каноническое имя refractor'а. */
const LANG_ALIASES: Record<string, string> = {
  py: "python",
  py3: "python",
  js: "javascript",
  jsx: "javascript",
  ts: "typescript",
  tsx: "typescript",
  sh: "bash",
  shell: "bash",
  console: "bash",
  zsh: "bash",
  c: "cpp",
  "c++": "cpp",
  yml: "yaml",
};
const SUPPORTED = new Set(Object.values(LANG_ALIASES));

interface CodeBlockProps {
  lang: string;
  children?: ReactNode;
}

/** Рекурсивно собирает текст из детей React-элемента (для копирования кода). */
function extractText(node: ReactNode): string {
  if (node == null || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(extractText).join("");
  if (isValidElement<{ children?: ReactNode }>(node)) return extractText(node.props.children);
  return "";
}

/** Блочный код: шапка с языком и кнопкой «Копировать». */
function CodeBlock({ lang, children }: CodeBlockProps) {
  const code = extractText(children).replace(/\n$/, "");
  const [copied, setCopied] = useState(false);
  const normalized = LANG_ALIASES[lang.toLowerCase()] ?? lang.toLowerCase();
  const supported = SUPPORTED.has(normalized);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      // clipboard недоступен — просто игнорируем
    }
  };

  return (
    <div className="my-6 overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="flex items-center justify-between gap-3 border-b border-slate-200 bg-slate-50 px-4 py-2">
        <span className="font-mono text-[11px] uppercase tracking-wider text-slate-500">{lang}</span>
        <button
          type="button"
          onClick={handleCopy}
          aria-label="Скопировать код"
          className="inline-flex cursor-pointer items-center gap-1.5 rounded-md px-2 py-1 font-mono text-[11px] text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
        >
          {copied ? (
            <Check className="h-3.5 w-3.5 text-emerald-600" />
          ) : (
            <Copy className="h-3.5 w-3.5" />
          )}
          {copied ? "Скопировано" : "Копировать"}
        </button>
      </div>
      <SyntaxHighlighter
        language={supported ? normalized : undefined}
        style={oneLight}
        customStyle={{ margin: 0, padding: "1rem 1.25rem", fontSize: "13px", background: "#ffffff" }}
        codeTagProps={{
          style: { fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" },
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

/** Кастомные рендереры для react-markdown: код, таблицы, ссылки и директивы. */
const components = {
  pre({ children }: { children?: ReactNode }) {
    const element = isValidElement<{ className?: string; children?: ReactNode }>(children)
      ? children
      : null;
    const language =
      element && typeof element.props.className === "string"
        ? /language-([\w+-]+)/.exec(element.props.className)?.[1] ?? "код"
        : "код";
    return <CodeBlock lang={language}>{children}</CodeBlock>;
  },

  code(props: { className?: string; children?: ReactNode }) {
    const isBlock = /language-/.test(props.className ?? "");
    if (isBlock) {
      return <code>{props.children}</code>;
    }
    return (
      <code
        {...props}
        className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-[0.85em] text-slate-800 font-medium whitespace-pre-wrap break-words border border-slate-200"
      >
        {props.children}
      </code>
    );
  },

  table({ children }: { children?: ReactNode }) {
    return (
      <div className="my-5 overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm text-slate-700">{children}</table>
      </div>
    );
  },

  a({ children, href }: { children?: ReactNode; href?: string }) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noreferrer"
        className="text-indigo-600 underline decoration-indigo-300 underline-offset-2 transition hover:text-indigo-500"
      >
        {children}
      </a>
    );
  },

  // Директивы `:::` (callout'ы и вкладки) обрабатываются пре-токенизатором
  // splitSegments ниже и не попадают в react-markdown.
} as unknown as Components;

interface MarkdownArticleProps {
  markdown: string;
  className?: string;
}

/** Результат пре-токенизации: обычный markdown или структурированный блок. */
type Segment =
  | { kind: "md"; content: string }
  | { kind: "callout"; type: CalloutType; title?: string; content: string }
  | { kind: "tabs"; tabs: Array<{ title?: string; content: string }> }
  | {
      kind: "ext";
      directive: "interview" | "complexity" | "quiz" | "solution";
      title?: string;
      content: string;
    };

/** Дополнительные директивы, обрабатываемые продвинутыми блоками (не классическим Callout). */
const EXT_DIRECTIVES = new Set(["interview", "complexity", "quiz", "solution"]);

function cleanTitle(raw: string): string {
  let t = raw.trim();
  // Поддержка синтаксиса `:::callout[Заголовок]` (а также кавычек/прочего).
  const bracketed = /^\[(.*)\]$/.exec(t);
  if (bracketed) t = bracketed[1];
  return t.replace(/^["']|["']$/g, "").trim();
}

/**
 * Разбирает `:::quiz` блок: вопрос — первая строка, варианты — `- [ ] текст — пояснение`.
 * `- [x]`/`- [X]` помечает **правильный** вариант.
 */
function parseInlineQuiz(content: string): QuizQuestion {
  const questionParts: string[] = [];
  const options: QuizOption[] = [];
  let n = 0;

  for (const raw of content.split("\n")) {
    const t = raw.trim();
    if (!t) continue;
    const m = /^[-*]\s*\[([ xX])\]\s*(.*)$/.exec(t);
    if (m) {
      const isCorrect = m[1].toLowerCase() === "x";
      const rest = m[2].trim();
      const dash = rest.search(/[\u2014\u2013]/); // — em/en dash
      const text = dash === -1 ? rest : rest.slice(0, dash).trim();
      const explanation = dash === -1 ? "" : rest.slice(dash + 1).trim();
      options.push({ id: String(n++), text, isCorrect, explanation });
    } else {
      questionParts.push(t.replace(/\*\*/g, ""));
    }
  }

  return {
    id: "inline-quiz",
    question: questionParts.join(" ").trim() || "Проверьте себя",
    options,
  };
}

/** Собирает строки блока до закрывающего `:::`, не путая `:::` внутри кода. */
function collectContent(lines: string[], from: number): { content: string; endIndex: number } {
  const out: string[] = [];
  let inCode = false;
  let j = from;
  while (j < lines.length) {
    const t = lines[j].trim();
    if (/^```/.test(t)) inCode = !inCode;
    if (!inCode && t === ":::") {
      return { content: out.join("\n").replace(/\n+$/, ""), endIndex: j + 1 };
    }
    out.push(lines[j]);
    j++;
  }
  return { content: out.join("\n").replace(/\n+$/, ""), endIndex: j };
}

function parseBlock(
  lines: string[],
  start: number,
  name: string,
  arg: string,
): { segment: Segment; nextIndex: number } {
  // Вкладки: внутри могут быть только `:::tab ... :::` блоки, закрываются `:::`.
  if (name === "tabs") {
    const tabs: Array<{ title?: string; content: string }> = [];
    let j = start + 1;
    while (j < lines.length) {
      const t = lines[j].trim();
      if (t === "") { j++; continue; }
      if (t === ":::") return { segment: { kind: "tabs", tabs }, nextIndex: j + 1 };
      const tabOpen = /^:{3}\s*tab(?:\s+(.*))?$/.exec(t);
      if (tabOpen) {
        const title = cleanTitle(tabOpen[1] ?? "");
        const body = collectContent(lines, j + 1);
        tabs.push({ ...(title ? { title } : {}), content: body.content });
        j = body.endIndex;
      } else {
        j++;
      }
    }
    return { segment: { kind: "tabs", tabs }, nextIndex: j };
  }

  // Одиночный блок (callout): содержимое до закрывающего `:::`, заголовок — из строки открытия.
  const body = collectContent(lines, start + 1);
  const title = cleanTitle(arg);

  // Продвинутые директивы (interview/complexity/quiz/solution) — отдельные блоки.
  if (EXT_DIRECTIVES.has(name)) {
    return {
      segment: {
        kind: "ext",
        directive: name as "interview" | "complexity" | "quiz" | "solution",
        ...(title ? { title } : {}),
        content: body.content,
      },
      nextIndex: body.endIndex,
    };
  }

  return {
    segment: {
      kind: "callout",
      type: name as CalloutType,
      ...(title ? { title } : {}),
      content: body.content,
    },
    nextIndex: body.endIndex,
  };
}

/** Разбирает markdown на сегменты, выделяя `:::callout` и `:::tabs`. */
function splitSegments(markdown: string): Segment[] {
  const lines = markdown.split("\n");
  const segments: Segment[] = [];
  let md = "";
  let i = 0;
  let inCode = false;

  const pushMd = () => {
    const content = md.replace(/\n+$/, "");
    if (content !== "") segments.push({ kind: "md", content });
    md = "";
  };

  while (i < lines.length) {
    const trimmed = lines[i].trim();
    if (/^```/.test(trimmed)) { inCode = !inCode; md += lines[i] + "\n"; i++; continue; }
    if (!inCode) {
      const open = /^:{3}\s*([a-zA-Z][\w-]*)(?:\s+(.*))?$/.exec(trimmed);
      if (open) {
        pushMd();
        const parsed = parseBlock(lines, i, open[1], open[2] ?? "");
        segments.push(parsed.segment);
        i = parsed.nextIndex;
        continue;
      }
    }
    md += lines[i] + "\n";
    i++;
  }
  pushMd();
  return segments;
}

/** markdown-фрагмент со стилями prose и подсветкой кода. */
function MarkdownContent({ content }: { content: string }) {
  return (
    <div className="markdown-body prose prose-slate max-w-none prose-headings:text-slate-900 prose-strong:text-slate-900 prose-a:text-indigo-600 prose-code:font-mono prose-code:text-[0.85em] prose-code:before:content-none prose-code:after:content-none prose-blockquote:border-l-indigo-400 prose-blockquote:text-slate-600 prose-th:text-slate-900 prose-hr:border-slate-200">
      <Markdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </Markdown>
    </div>
  );
}

/**
 * Рендер markdown-контента (лекции, условия задач): базовые стили prose,
 * подсветка кода с копированием, таблицы, callout'ы (:::) и вкладки (:::tabs).
 */
export function MarkdownArticle({ markdown, className = "" }: MarkdownArticleProps) {
  const segments = useMemo(() => splitSegments(markdown), [markdown]);
  return (
    <div className={className}>
      {segments.map((seg, i) => {
        if (seg.kind === "md") return <MarkdownContent key={i} content={seg.content} />;
        if (seg.kind === "tabs") {
          return (
            <Tabs key={i}>
              {seg.tabs.map((tab, ti) => (
                <TabPanel key={ti} title={tab.title}>
                  <MarkdownContent content={tab.content} />
                </TabPanel>
              ))}
            </Tabs>
          );
        }
        if (seg.kind === "ext") {
          if (seg.directive === "quiz") {
            return <QuizBlock key={i} question={parseInlineQuiz(seg.content)} />;
          }
          return (
            <CalloutBlock key={i} type={seg.directive} title={seg.title}>
              <MarkdownContent content={seg.content} />
            </CalloutBlock>
          );
        }
        return (
          <Callout key={i} type={seg.type} title={seg.title}>
            <MarkdownContent content={seg.content} />
          </Callout>
        );
      })}
    </div>
  );
}