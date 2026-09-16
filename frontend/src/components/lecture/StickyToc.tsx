import { useScrollSpy } from "./useScrollSpy";

export interface TocItem {
  id: string;
  text: string;
  level: number;
}

/** Липкое оглавление по H2/H3 с подсветкой текущего раздела (desktop). */
export function StickyToc({ items }: { items: TocItem[] }) {
  const activeId = useScrollSpy(items.map(i => `#${i.id}`));
  if (items.length === 0) return null;

  return (
    <nav className="hidden max-h-[70vh] space-y-1 overflow-auto text-sm lg:block" aria-label="Оглавление">
      {items.map(item => (
        <a
          key={item.id}
          href={`#${item.id}`}
          style={{ paddingLeft: 8 + (item.level - 2) * 12 }}
          className={`block border-l-2 py-1 transition ${
            activeId === item.id
              ? "border-indigo-500 font-medium text-indigo-700"
              : "border-slate-200 text-slate-500 hover:text-slate-800"
          }`}
        >
          {item.text}
        </a>
      ))}
    </nav>
  );
}