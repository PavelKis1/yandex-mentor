import type { ReactNode } from "react";
import { Accordion } from "../common/Accordion";

type Variant = "note" | "tip" | "warning" | "danger" | "interview" | "complexity";

interface CalloutBlockProps {
  type: string;
  title?: string;
  children?: ReactNode;
}

const META: Record<Variant, { accent: string; icon: string }> = {
  note: { accent: "border-blue-200 bg-blue-50", icon: "📝" },
  tip: { accent: "border-emerald-200 bg-emerald-50", icon: "💡" },
  warning: { accent: "border-amber-200 bg-amber-50", icon: "⚠️" },
  danger: { accent: "border-red-200 bg-red-50", icon: "🚨" },
  interview: { accent: "border-violet-200 bg-violet-50", icon: "🎤" },
  complexity: { accent: "border-violet-200 bg-violet-50", icon: "⚙️" },
};

/**
 * Расширенная выноска. Для `interview` — свёрнутый аккордеон («вопрос с собеседования»),
 * для `complexity` — карточка асимптотики. Остальные варианты — классический блок.
 */
export function CalloutBlock({ type, title, children }: CalloutBlockProps) {
  if (type === "interview") {
    return <Accordion title={title || "Вопрос с собеседования"}>{children}</Accordion>;
  }

  const meta = META[type as Variant] ?? META.note;
  const heading = type === "complexity" ? "Асимптотическая сложность" : title;
  return (
    <div className={`my-4 rounded-xl border border-solid p-4 ${meta.accent}`}>
      <div className="mb-2 flex items-center gap-2 font-semibold text-slate-900">
        <span aria-hidden>{meta.icon}</span>
        <span>{heading}</span>
      </div>
      <div className="text-slate-700">{children}</div>
    </div>
  );
}