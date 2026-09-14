import { useState, type ReactNode } from "react";
import { ChevronDown, Lock, Unlock } from "lucide-react";

interface SpoilerProps {
  title: string;
  /** Дополнительная подсказка под заголовком (до раскрытия). */
  note?: string;
  defaultOpen?: boolean;
  children: ReactNode;
}

/**
 * Сворачиваемый блок-спойлер: по умолчанию закрыт, чтобы не подсвечивать
 * готовые решения раньше времени. Используется для «Базового кода»
 * и прочих разделов лекций с почти-решениями.
 */
export function Spoiler({ title, note, defaultOpen = false, children }: SpoilerProps) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="overflow-hidden rounded-xl border border-indigo-500/25 bg-indigo-500/[0.04]">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-3 bg-indigo-500/10 px-4 py-3 text-left transition hover:bg-indigo-500/15 cursor-pointer"
      >
        <span className="flex items-center gap-2 text-sm font-semibold text-indigo-700">
          {open ? <Unlock className="h-4 w-4 shrink-0" /> : <Lock className="h-4 w-4 shrink-0" />}
          <span>{title}</span>
        </span>
        <ChevronDown
          className={`h-4 w-4 shrink-0 text-indigo-500 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {!open && note && <p className="px-4 pb-3 text-[11px] text-slate-500">{note}</p>}

      {open && <div className="px-4 pt-2 pb-4">{children}</div>}
    </div>
  );
}