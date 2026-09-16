import { Children, isValidElement, useState, type ReactNode } from "react";

export interface TabPanelProps {
  title?: string;
  children?: ReactNode;
}

/** Внутренняя «панель» вкладки — рендерит только своё содержимое. */
export function TabPanel({ children }: TabPanelProps) {
  return <>{children}</>;
}

interface TabsProps {
  children?: ReactNode;
}

/** Канонические названия вкладок → русские подписи. */
const LABELS: Record<string, string> = {
  condition: "Условие",
  solution: "Решение",
  instructions: "Инструкция",
  example: "Пример",
};

/**
 * Группа вкладок (треугольник) в markdown, задаётся директивами:
 * :::tabs
 * :::tab title="Условие"  ...  :::
 * :::tab title="Решение"  ...  :::
 * :::
 */
export function Tabs({ children }: TabsProps) {
  const items = Children.toArray(children).filter((child) =>
    isValidElement<TabPanelProps>(child),
  ) as Array<React.ReactElement<TabPanelProps>>;

  const [active, setActive] = useState(0);
  if (items.length === 0) return null;
  const safe = Math.min(active, items.length - 1);

  return (
    <div className="my-6 overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="flex flex-wrap gap-1 border-b border-slate-200 bg-slate-50 px-2 pt-2">
        {items.map((item, i) => {
          const raw = item.props.title ?? "";
          const title = LABELS[raw.toLowerCase()] ?? (raw || `Вкладка ${i + 1}`);
          return (
            <button
              key={i}
              type="button"
              role="tab"
              aria-selected={safe === i}
              onClick={() => setActive(i)}
              className={`rounded-t-lg px-4 py-2 text-xs font-semibold transition cursor-pointer ${
                safe === i
                  ? "-mb-px border border-slate-200 border-b-white bg-white text-indigo-700"
                  : "text-slate-500 hover:bg-slate-100 hover:text-slate-700"
              }`}
            >
              {title}
            </button>
          );
        })}
      </div>
      <div className="p-5">{items[safe]}</div>
    </div>
  );
}