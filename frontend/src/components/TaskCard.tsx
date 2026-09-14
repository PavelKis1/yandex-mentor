import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  ArrowRight,
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

  let statusBg = "bg-white border-slate-300 hover:border-slate-400 text-slate-900";
  let statusIcon = <Circle className="h-4 w-4 text-slate-600" />;
  let badgeText = "К изучению";
  let badgeClass = "bg-slate-200 text-slate-800";

  if (status === "done") {
    statusBg = "bg-emerald-50 border-emerald-200 hover:border-emerald-300 text-emerald-900";
    statusIcon = <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
    badgeText = "Пройдено";
    badgeClass = "bg-emerald-100 text-emerald-700";
  } else if (status === "wip") {
    statusBg = "bg-indigo-50 border-indigo-200 hover:border-indigo-300 text-indigo-950";
    statusIcon = <Clock className="h-4 w-4 text-indigo-700" />;
    badgeText = "В процессе";
    badgeClass = "bg-indigo-100 text-indigo-800";
  }

  return (
    <div
      onClick={() => onSelect(task)}
      onContextMenu={(event) => {
        event.preventDefault();
        setMenuOpen(true);
      }}
      title={onSetStatus ? "Открыть тему. ПКМ — быстро сменить статус" : undefined}
      className={`group relative flex flex-col justify-between p-5 rounded-2xl border transition-all duration-200 cursor-pointer shadow-md hover:shadow-xl hover:-translate-y-1 ${statusBg}`}
    >
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-mono bg-slate-100 px-2.5 py-1 rounded-lg text-slate-700 border border-slate-200">
            #{task.id}
          </span>
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${badgeClass}`}>
            {badgeText}
          </span>
        </div>
        <h3 className="font-semibold text-sm line-clamp-2 group-hover:text-indigo-500 transition">
          {task.name}
        </h3>
      </div>

      <div className="flex items-center justify-between mt-6 pt-3 border-t border-slate-200 text-xs text-slate-500">
        <span className="flex items-center gap-1.5">
          {statusIcon}
          <span>Материалы</span>
        </span>
        <span className="flex items-center gap-2">
          {onSetStatus && (
            <button
              type="button"
              onClick={(event) => {
                event.stopPropagation();
                setMenuOpen((open) => !open);
              }}
              aria-label="Сменить статус"
              title="Быстро сменить статус (todo / wip / done)"
              className="flex items-center gap-1 rounded-lg px-1.5 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-indigo-700 transition cursor-pointer"
            >
              <MoreHorizontal className="w-4 h-4" />
            </button>
          )}
          <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-500 group-hover:translate-x-1 transition" />
        </span>
      </div>

      {/* Контекстное меню статуса */}
      {menuOpen && (
        <div
          ref={menuRef}
          onClick={(event) => event.stopPropagation()}
          className="absolute right-3 bottom-14 z-30 w-44 rounded-xl border border-slate-200 bg-white p-1 shadow-xl"
        >
          <p className="px-3 py-1.5 text-[10px] uppercase tracking-wider text-slate-500">
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