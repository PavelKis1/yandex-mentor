import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Lightbulb,
  Terminal,
} from "lucide-react";
import type { ProblemPublic, RunResponse, SubmitResponse } from "../types";
import { readJson, writeJson } from "../utils/storage";
import { MarkdownArticle } from "./MarkdownArticle";
import { SolutionEditor } from "./SolutionEditor";

const HINTS_KEY = (problemId: string) => `hints:${problemId}`;

interface ProblemWorkbenchProps {
  problem: ProblemPublic;
  /** 0-based порядковый номер задачи в лекции. */
  index: number;
  total: number;
  lectureName: string;
  submitting: boolean;
  result: RunResponse | SubmitResponse | null;
  onRun: (code: string) => void;
  onSubmit: (code: string) => void;
  onPrev: (() => void) | null;
  onNext: (() => void) | null;
  /** Вернуться к списку задач лекции. */
  onBack: () => void;
}

const DIFF_META: Record<
  "easy" | "medium" | "hard",
  { label: string; className: string }
> = {
  easy: {
    label: "Простая",
    className: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30",
  },
  medium: {
    label: "Средняя",
    className: "bg-amber-500/20 text-amber-300 border border-amber-500/30",
  },
  hard: {
    label: "Сложная",
    className: "bg-red-500/20 text-red-300 border border-red-500/30",
  },
};

/**
 * Воркбенч LeetCode-стиля: слева условие (описание/примеры/ограничения/подсказки),
 * справа решётка из Monaco-редактора и консоли результатов.
 */
export function ProblemWorkbench({
  problem,
  index,
  total,
  lectureName,
  submitting,
  result,
  onRun,
  onSubmit,
  onPrev,
  onNext,
  onBack,
}: ProblemWorkbenchProps) {
  const totalHints = problem.hints?.length ?? 0;
  const [unlocked, setUnlocked] = useState<number>(
    () => readJson<number>(HINTS_KEY(problem.id)) ?? 0,
  );

  useEffect(() => {
    writeJson(HINTS_KEY(problem.id), unlocked);
  }, [problem.id, unlocked]);

  const diffMeta = DIFF_META[problem.difficulty];
  const shownHints = (problem.hints ?? []).slice(0, unlocked);

  return (
    <div className="space-y-4">
      {/* Header: навигация по задачам лекции */}
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800/70 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:bg-slate-700 cursor-pointer"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          К списку
        </button>
        <span className="text-[11px] font-mono text-slate-500">
          {lectureName} • Задание {index + 1} / {total}
        </span>
        <span className={`ml-auto text-[10px] font-semibold shrink-0 px-2.5 py-1 rounded-full ${diffMeta.className}`}>
          {diffMeta.label}
        </span>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,5fr)_minmax(0,6fr)] gap-4 items-start">
        {/* Левая панель — условие */}
        <div className="min-w-0 space-y-4">
          <h2 className="flex items-start gap-2.5 text-lg font-bold text-white">
            <Terminal className="h-5 w-5 shrink-0 text-amber-400 mt-0.5" />
            {problem.title}
            {problem.solved && (
              <span className="mt-1 text-[10px] font-semibold text-emerald-400 bg-emerald-500/15 px-2 py-0.5 rounded-full border border-emerald-500/30 shrink-0">
                ✓ Решено
              </span>
            )}
          </h2>

          <div className="markdown-body text-sm leading-relaxed text-slate-300">
            <MarkdownArticle markdown={problem.description} />
          </div>
{/* Примеры */}
          {problem.examples && problem.examples.length > 0 && (
            <div className="space-y-3">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-white">
                Примеры
              </h3>
              {problem.examples.map((example: { input?: string; output?: string; explanation?: string }, i: number) => (
                <div
                  key={i}
                  className="rounded-xl border border-slate-800 bg-slate-950/50 overflow-hidden"
                >
                  <div className="px-4 py-2 border-b border-slate-800 text-[10px] font-mono text-slate-500">
                    Пример {i + 1}
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 text-xs font-mono">
                    <div className="px-4 py-3 border-b sm:border-b-0 sm:border-r border-slate-800">
                      <span className="text-slate-500 block mb-1 text-[10px] uppercase">Input</span>
                      <code className="text-slate-200 whitespace-pre">{example.input ?? ""}</code>
                    </div>
                    <div className="px-4 py-3">
                      <span className="text-slate-500 block mb-1 text-[10px] uppercase">Output</span>
                      <code className="text-emerald-400 whitespace-pre">{example.output ?? ""}</code>
                    </div>
                  </div>
                  {example.explanation && (
                    <div className="px-4 py-2 border-t border-slate-800 text-[11px] text-slate-400 bg-slate-900/50">
                      <span className="text-slate-500">Пояснение:</span> {example.explanation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Ограничения */}
          {problem.constraints && problem.constraints.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-white">Ограничения</h3>
              <ul className="space-y-1 pl-4">
                {problem.constraints.map((c: string, i: number) => (
                  <li key={i} className="text-xs text-slate-400 list-disc">{c}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Подсказки с учётом необратимости */}
          {totalHints > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-white">Подсказки ментора</h3>
              {shownHints.length > 0 && (
                <div className="bg-amber-500/10 border border-amber-500/25 p-3 rounded-xl text-xs space-y-1">
                  {shownHints.map((hint, i) => (
                    <div key={i} className="flex items-start gap-1.5 text-amber-200/90">
                      <Lightbulb className="w-3.5 h-3.5 shrink-0 text-amber-500/70 mt-0.5" />
                      {hint}
                    </div>
                  ))}
                </div>
              )}

              {unlocked < totalHints && (
                <button
                  type="button"
                  onClick={() => setUnlocked((c) => c + 1)}
                  className="flex items-center gap-1.5 w-full border border-dashed border-amber-500/40 bg-amber-500/[0.04] hover:bg-amber-500/10 rounded-xl px-3 py-2 text-xs font-medium text-amber-300 transition cursor-pointer"
                >
                  <Lightbulb className="w-3.5 h-3.5" />
                  Показать подсказку {unlocked + 1} из {totalHints}
                  <span className="ml-auto text-[10px] text-slate-500">необратимо</span>
                </button>
              )}
            </div>
          )}

          {/* Навигация между задачами */}
          {(onPrev || onNext) && (
            <div className="flex items-center justify-between border-t border-slate-800 pt-3">
              {onPrev ? (
                <button
                  onClick={onPrev}
                  className="flex items-center gap-1.5 rounded-xl border border-slate-700 bg-slate-800/70 px-3 py-1.5 text-xs font-medium text-slate-200 transition hover:bg-slate-700 cursor-pointer"
                >
                  <ChevronLeft className="h-3.5 w-3.5" />
                  Предыдущая
                </button>
              ) : <span />}
              {onNext ? (
                <button
                  onClick={onNext}
                  className="flex items-center gap-1.5 rounded-xl bg-amber-500 px-3 py-1.5 text-xs font-semibold text-slate-950 transition hover:bg-amber-400 cursor-pointer"
                >
                  Следующая
                  <ChevronRight className="h-3.5 w-3.5" />
                </button>
              ) : <span />}
            </div>
          )}
        </div>

        {/* Правая панель — редактор */}
        <div className="min-w-0">
          <SolutionEditor
            problem={problem}
            submitting={submitting}
            result={result}
            onRun={onRun}
            onSubmit={onSubmit}
          />
        </div>
      </div>
    </div>
  );
}