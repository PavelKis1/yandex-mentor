import type { InterviewCheatSheet } from "../../types";

/** Шпаргалка «Ответ на собеседовании за 60 секунд» — отображается в конце лекции. */
export function CheatSheetBlock({ data }: { data: InterviewCheatSheet }) {
  if (!data || !data.summary60Sec?.length) return null;

  return (
    <div className="mt-8 rounded-xl border-2 border-dashed border-amber-300 bg-amber-50/50 p-5">
      <h2 className="mb-3 text-lg font-bold text-slate-900">
        ⏱️ Ответ на собеседовании за 60 секунд
      </h2>
      <ul className="list-inside list-disc space-y-1 text-slate-700">
        {data.summary60Sec.map((point, i) => (
          <li key={i}>{point}</li>
        ))}
      </ul>
    </div>
  );
}