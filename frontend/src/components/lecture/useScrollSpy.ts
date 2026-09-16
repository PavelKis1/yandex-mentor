import { useEffect, useState } from "react";

/** Отслеживает, какой заголовок (по CSS-селекторам) сейчас в области чтения. */
export function useScrollSpy(selectors: string[]): string {
  const ids = selectors.map(s => s.replace(/^#/, "")).filter(Boolean);
  const key = ids.join("|");
  const [activeId, setActiveId] = useState<string>(ids[0] ?? "");

  useEffect(() => {
    if (ids.length === 0) return;
    const onScroll = () => {
      let current = "";
      for (const id of ids) {
        const el = document.getElementById(id);
        if (!el) continue;
        const top = el.getBoundingClientRect().top;
        if (top <= 150) current = id; // последний (по порядку) пройденный заголовок
      }
      setActiveId(current || ids[0]);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  return activeId;
}