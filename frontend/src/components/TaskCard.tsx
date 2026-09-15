import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  CheckCircle2,
  Circle,
  Clock,
  MoreHorizontal,
} from "lucide-react";
import type { TaskStatus, TaskSummary } from "../types";

interface TaskCardProps {
  task: TaskSummary;
  status: TaskStatus;
  onSelect: (task: TaskSummary) => void;
  /** Быстрая смена статуса (ПКМ или кнопка «···»). */
  onSetStatus?: (taskId: string, status: TaskStatus) => void;
}

const STATUS_ITEMS: { value: TaskStatus; label: string; icon: ReactNode; activeClass: string }[] = [
  {
    value: "todo",
    label: "К изучению",
    icon: <Circle className="h-4 w-4" />,
    activeClass: "bg-slate-100 text-slate-800",
  },
  {
    value: "wip",
    label: "В процессе",
    icon: <Clock className="h-4 w-4 text-indigo-600" />,
    activeClass: "bg-indigo-100 text-indigo-800",
  },
  {
    value: "done",
    label: "Пройдено",
    icon: <CheckCircle2 className="h-4 w-4 text-emerald-600" />,
    activeClass: "bg-emerald-100 text-emerald-800",
  },
];

export function TaskCard({ task, status, onSelect, onSetStatus }: TaskCardProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement | null>(null);

  // Закрытие меню по клику вне и по Esc.
  useEffect(() => {
    if (!menuOpen) return;
    const handlePointerDown = (event: MouseEvent) => {
      if (menuRef.current && event.target instanceof Node && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    };
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setMenuOpen(false);
    };
    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [menuOpen]);

  const applyStatus = (value: TaskStatus) => {
    onSetStatus?.(task.id, value);
    setMenuOpen(false);
  };

  let cardBg = "bg-white border-slate-200 text-slate-900 hover:border-slate-300";
  let statusIcon = <Circle className="h-5 w-5 text-slate-300" />;
  let badgeText = "К изучению";
  let badgeClass = "bg-slate-100 text-slate-600 border border-slate-200";
  const orderLabel = String(task.id).padStart(2, "0");

  if (status === "done") {
    cardBg = "bg-emerald-50/60 border-emerald-200 text-emerald-950 hover:border-emerald-300";
    statusIcon = <CheckCircle2 className="w-5 h-5 text-emerald-600" />;
    badgeText = "Пройдено";
    badgeClass = "bg-emerald-100 text-emerald-700 border border-emerald-200";
  } else if (status === "wip") {
    cardBg = "bg-indigo-50/60 border-indigo-200 text-indigo-950 hover:border-indigo-300";
    statusIcon = <Clock className="h-5 w-5 text-indigo-600" />;
    badgeText = "В процессе";
    badgeClass = "bg-indigo-100 text-indigo-700 border border-indigo-200";
  }

  return (
    <div
      onClick={() => onSelect(task)}
      onContextMenu={(event) => {
        event.preventDefault();
        setMenuOpen(true);
      }}
      title={onSetStatus ? "Открыть тему. ПКМ — быстро сменить статус" : undefined}
      className={`group relative flex flex-col p-5 rounded-2xl border transition-all duration-300 cursor-pointer shadow-sm hover:shadow-lg hover:-translate-y-1 ${cardBg}`}
    >
      <div className="flex items-center justify-between mb-4">
        <span className="text-xs font-mono font-bold tracking-wide text-slate-600">
          #{orderLabel}
        </span>
        <div className={`text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider ${badgeClass}`}>
          {badgeText}
        </div>
      </div>
      
      <h3 className="font-semibold text-sm text-slate-900 group-hover:text-indigo-700 transition-colors duration-200 flex-grow">
        {task.name}
      </h3>

      <div className="flex items-center justify-between mt-5 pt-4 border-t border-slate-200/50">
        <div className="flex items-center gap-1.5 text-slate-500">
          {statusIcon}
        </div>
        
        {onSetStatus && (
           <button
             type="button"
             onClick={(event) => {
               event.stopPropagation();
               setMenuOpen((open) => !open);
             }}
             className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-slate-200/50 rounded-lg transition-opacity"
           >
             <MoreHorizontal className="w-4 h-4 text-slate-500" />
           </button>
        )}
      </div>

      {/* Контекстное меню статуса */}
      {menuOpen && (
        <div
          ref={menuRef}
          onClick={(event) => event.stopPropagation()}
          className="absolute right-3 bottom-16 z-30 w-44 rounded-xl border border-slate-200 bg-white p-1 shadow-xl animate-in fade-in zoom-in-95 duration-200"
        >
          <p className="px-3 py-1.5 text-[10px] uppercase tracking-wider text-slate-400">
            Статус темы
          </p>
          {STATUS_ITEMS.map((item) => {
            const active = item.value === status;
            return (
              <button
                key={item.value}
                type="button"
                onClick={() => applyStatus(item.value)}
                className={`flex w-full cursor-pointer items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition ${
                  active ? item.activeClass : "text-slate-700 hover:bg-slate-100"
                }`}
              >
                {item.icon}
                {item.label}
                {active && (
                  <span className="ml-auto text-[10px] font-semibold text-current">✓</span>
                )}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );

}

