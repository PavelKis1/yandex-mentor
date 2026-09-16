import { AlertTriangle, Info, Lightbulb, XCircle } from "lucide-react";
import type { ReactNode } from "react";

export type CalloutType = "note" | "tip" | "warning" | "danger";

const META: Record<
  CalloutType,
  {
    icon: typeof Info;
    border: string;
    bg: string;
    iconColor: string;
    titleColor: string;
    bodyColor: string;
  }
> = {
  note: {
    icon: Info,
    border: "border-sky-200",
    bg: "bg-sky-50",
    iconColor: "text-sky-600",
    titleColor: "text-sky-800",
    bodyColor: "text-sky-900/80",
  },
  tip: {
    icon: Lightbulb,
    border: "border-emerald-200",
    bg: "bg-emerald-50",
    iconColor: "text-emerald-600",
    titleColor: "text-emerald-800",
    bodyColor: "text-emerald-900/80",
  },
  warning: {
    icon: AlertTriangle,
    border: "border-amber-200",
    bg: "bg-amber-50",
    iconColor: "text-amber-600",
    titleColor: "text-amber-800",
    bodyColor: "text-amber-900/80",
  },
  danger: {
    icon: XCircle,
    border: "border-red-200",
    bg: "bg-red-50",
    iconColor: "text-red-600",
    titleColor: "text-red-800",
    bodyColor: "text-red-900/80",
  },
};

interface CalloutProps {
  type?: CalloutType;
  title?: string;
  children?: ReactNode;
}

/**
 * Информационный блок (callout) в markdown, задаётся директивой:
 * :::note  /  :::tip  /  :::warning  /  :::danger  (+ опциональный :::title)
 */
export function Callout({ type = "note", title, children }: CalloutProps) {
  const meta = META[type] ?? META.note;
  const Icon = meta.icon;
  return (
    <div className={`my-6 flex gap-3 rounded-xl border ${meta.border} ${meta.bg} p-4`}>
      <Icon className={`mt-0.5 h-5 w-5 shrink-0 ${meta.iconColor}`} />
      <div className="min-w-0 flex-1">
        {title && <p className={`mb-1 text-sm font-bold ${meta.titleColor}`}>{title}</p>}
        <div className={`space-y-2 text-sm ${meta.bodyColor}`}>{children}</div>
      </div>
    </div>
  );
}