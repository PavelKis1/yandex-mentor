import { useState } from "react";
import type { QuizQuestion } from "../../types";

/** Интерактивный мини-тест: выбор варианта с объяснением. */
export function QuizBlock({ question }: { question: QuizQuestion }) {
  const [selected, setSelected] = useState<string | null>(null);
  if (!question?.options?.length) return null;

  return (
    <div className="my-4 rounded-xl border border-indigo-100 bg-indigo-50/50 p-4">
      <p className="mb-3 font-semibold text-slate-900">🎯 {question.question}</p>
      <div className="space-y-2">
        {question.options.map(opt => {
          const chosen = selected === opt.id;
          const showCorrect = selected !== null && opt.isCorrect;
          const showWrong = chosen && !opt.isCorrect;
          return (
            <button
              key={opt.id}
              onClick={() => setSelected(opt.id)}
              className={`w-full rounded-lg border p-3 text-left transition ${
                showCorrect
                  ? "border-emerald-300 bg-emerald-50"
                  : showWrong
                    ? "border-red-300 bg-red-50"
                    : chosen
                      ? "border-slate-300 bg-slate-100"
                      : "border-slate-200 bg-white hover:border-indigo-300"
              }`}
            >
              <span className="inline-flex items-center gap-2">
                <span aria-hidden>{chosen ? (showCorrect ? "✅" : "❌") : "○"}</span>
                <span className="text-slate-800">{opt.text}</span>
              </span>
              {chosen && (
                <span className="mt-2 block text-sm text-slate-600">
                  {opt.explanation || (showCorrect ? "Верно!" : "")}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}