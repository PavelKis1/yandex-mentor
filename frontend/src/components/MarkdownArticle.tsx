import { useState, type ReactNode, isValidElement } from "react";
import Markdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { Check, Copy } from "lucide-react";

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
      <pre className="overflow-x-auto p-4 text-[13px] leading-relaxed whitespace-pre font-mono text-slate-800">
        {children}
      </pre>
    </div>
  );
}

/** Кастомные рендереры для react-markdown. */
const components: Components = {
  pre({ children }) {
    const element = isValidElement<{ className?: string; children?: ReactNode }>(children)
      ? children
      : null;
    const language =
      element && typeof element.props.className === "string"
        ? /language-([\w+-]+)/.exec(element.props.className)?.[1] ?? "код"
        : "код";
    return <CodeBlock lang={language}>{children}</CodeBlock>;
  },

  code(props) {
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

  table({ children }) {
    return (
      <div className="my-5 overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm text-slate-700">{children}</table>
      </div>
    );
  },

  a({ children, href }) {
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
};

interface MarkdownArticleProps {
  markdown: string;
  className?: string;
}

/**
 * Рендер markdown-контента (лекции, условия задач): базовые стили prose,
 * тёмные блоки кода с копированием, таблицы с горизонтальной прокруткой.
 */
export function MarkdownArticle({ markdown, className = "" }: MarkdownArticleProps) {
  return (
    <div
      className={`markdown-body prose prose-slate max-w-none prose-headings:text-slate-900 prose-strong:text-slate-900 prose-a:text-indigo-600 prose-code:font-mono prose-code:text-[0.85em] prose-code:before:content-none prose-code:after:content-none prose-blockquote:border-l-indigo-400 prose-blockquote:text-slate-600 prose-th:text-slate-900 prose-hr:border-slate-200 ${className}`}
    >
      <Markdown remarkPlugins={[remarkGfm]} components={components}>
        {markdown}
      </Markdown>
    </div>
  );
}