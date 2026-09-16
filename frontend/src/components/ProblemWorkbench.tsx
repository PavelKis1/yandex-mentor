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
  /** Сколько задач лекции уже решено и сколько всего — для индикатора прогресса. */
  solvedCount: number;
  solvedTotal: number;
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
    className: "bg-emerald-100 text-emerald-700 border border-emerald-200",
  },
  medium: {
    label: "Средняя",
    className: "bg-amber-100 text-amber-700 border border-amber-200",
  },
  hard: {
    label: "Сложная",
    className: "bg-red-100 text-red-700 border border-red-200",
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
  solvedCount,
  solvedTotal,
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
      <div className="flex flex-wrap items-center gap-3 bg-white rounded-xl border border-slate-200 p-3 shadow-sm">
        <button
          onClick={onBack}
          title={`Вернуться к заданиям лекции «${lectureName}»`}
          className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 transition hover:bg-slate-50 hover:border-slate-300 cursor-pointer shadow-sm"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          К списку
        </button>

        <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5">
          <button
            onClick={onPrev ?? undefined}
            disabled={!onPrev}
            className="text-slate-400 hover:text-slate-700 disabled:opacity-30 disabled:hover:text-slate-400 transition-colors cursor-pointer disabled:cursor-not-allowed"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <span className="text-xs font-semibold text-slate-700 min-w-[90px] text-center select-none">
            Задание {index + 1} <span className="text-slate-400 font-normal">из</span> {total}
          </span>
          <button
            onClick={onNext ?? undefined}
            disabled={!onNext}
            className="text-slate-400 hover:text-slate-700 disabled:opacity-30 disabled:hover:text-slate-400 transition-colors cursor-pointer disabled:cursor-not-allowed"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>

        {/* Мини-прогресс по заданиям темы */}
        <div
          className="flex items-center gap-2"
          title={`Решено задач в теме: ${solvedCount} из ${solvedTotal}`}
        >
          <div className="w-20 h-1.5 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full transition-all duration-500"
              style={{
                width: `${solvedTotal ? Math.round((solvedCount / solvedTotal) * 100) : 0}%`,
              }}
            />
          </div>
          <span className="text-[10px] font-semibold text-slate-600">
            {solvedCount}
            <span className="text-slate-400 font-normal">/{solvedTotal}</span>
          </span>
        </div>

        <span className={`ml-auto text-[10px] font-bold tracking-wider uppercase px-2.5 py-1 rounded-full ${diffMeta.className}`}>
          {diffMeta.label}
        </span>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,5fr)_minmax(0,6fr)] gap-4 items-start">
        {/* Левая панель — условие */}
        <div className="min-w-0 space-y-4">
          <h2 className="flex items-center gap-3 text-xl font-bold text-slate-900 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span className="bg-slate-900 text-white p-2 rounded-lg shadow-md shrink-0">
              <Terminal className="h-5 w-5" />
            </span>
            <span>Задача #{index + 1}: {problem.title}</span>
            {problem.solved && (
              <span className="ml-auto text-[10px] font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full border border-emerald-200 shrink-0">
                Решено
              </span>
            )}
          </h2>

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
            <MarkdownArticle markdown={problem.description} />
          </div>
{/* Примеры */}
          {problem.examples && problem.examples.length > 0 && (
            <div className="space-y-3">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-slate-900 pl-1">
                Примеры
              </h3>
              {problem.examples.map((example: { input?: string; output?: string; explanation?: string }, i: number) => (
                <div
                  key={i}
                  className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm"
                >
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                    Пример {i + 1}
                  </div>
                  <div className="space-y-2 font-mono text-sm">
                    <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
                      <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Вход:</span>
                      <div className="text-slate-800 mt-1 break-all">{example.input ?? ""}</div>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
                      <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Выход:</span>
                      <div className="text-slate-800 mt-1 break-all">{example.output ?? ""}</div>
                    </div>
                  </div>
                  {example.explanation && (
                    <div className="mt-3 text-xs text-slate-600 bg-indigo-50 border border-indigo-100 rounded-lg p-3">
                      <span className="font-semibold text-indigo-700">Пояснение:</span> {example.explanation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Ограничения */}
          {problem.constraints && problem.constraints.length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm space-y-2">
              <h3 className="text-sm font-semibold text-slate-900">Ограничения</h3>
              <ul className="space-y-1 pl-4">
                {problem.constraints.map((c: string, i: number) => (
                  <li key={i} className="text-xs text-slate-600 list-disc">{c}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Подсказки с учётом необратимости */}
          {totalHints > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm space-y-3">
              <h3 className="text-sm font-semibold text-slate-900">Подсказки ментора</h3>
              {shownHints.length > 0 && (
                <div className="bg-amber-50 border border-amber-200 p-3 rounded-xl text-xs space-y-2">
                  {shownHints.map((hint, i) => (
                    <div key={i} className="flex items-start gap-2 text-amber-800">
                      <Lightbulb className="w-3.5 h-3.5 shrink-0 text-amber-500 mt-0.5" />
                      {hint}
                    </div>
                  ))}
                </div>
              )}

              {unlocked < totalHints && (
                <button
                  type="button"
                  onClick={() => setUnlocked((c) => c + 1)}
                  className="flex items-center gap-1.5 w-full border border-dashed border-amber-300 bg-amber-50 hover:bg-amber-100 rounded-xl px-3 py-2 text-xs font-medium text-amber-700 transition cursor-pointer"
                >
                  <Lightbulb className="w-3.5 h-3.5" />
                  Показать подсказку {unlocked + 1} из {totalHints}
                  <span className="ml-auto text-[10px] text-slate-400">необратимо</span>
                </button>
              )}
            </div>
          )}

          {/* Навигация между задачами */}
          {(onPrev || onNext) && (
            <div className="flex items-center justify-between border-t border-slate-200 pt-3">
              {onPrev ? (
                <button
                  onClick={onPrev}
                  className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50 hover:border-slate-300 cursor-pointer shadow-sm"
                >
                  <ChevronLeft className="h-3.5 w-3.5" />
                  Предыдущая
                </button>
              ) : <span />}
              {onNext ? (
                <button
                  onClick={onNext}
                  className="flex items-center gap-1.5 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-indigo-500 cursor-pointer shadow-md"
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