import { useEffect, useState } from "react";
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Code,
  ListChecks,
  X,
} from "lucide-react";
import { useTask } from "../hooks/useTask";
import type {
  RunResponse,
  SubmitResponse,
  TaskStatus,
  TaskSummary,
} from "../types";
import { ErrorBanner } from "./ErrorBanner";
import { LectureView } from "./LectureView";
import { LoadingSpinner } from "./LoadingSpinner";
import { ProblemWorkbench } from "./ProblemWorkbench";

interface TopicModalProps {
  /** MP3-лекция из роадмапа: id = идентификатор лекции (темы), name = название. */
  lecture: TaskSummary;
  onClose: () => void;
  /** Обновление статуса темы в глобальном прогрессе после сабмита решения. */
  onTaskStatusChange?: (lectureId: string, status: TaskStatus) => void;
  /** Следующая тема по порядку — для кнопки «Дальше» в футере. */
  nextLecture?: TaskSummary | null;
  /** Переход на другую тему без закрытия модалки. */
  onOpenLecture?: (lecture: TaskSummary) => void;
}

type Tab = "lecture" | "tasks";

export function TopicModal({
  lecture,
  onClose,
  onTaskStatusChange,
  nextLecture,
  onOpenLecture,
}: TopicModalProps) {
  const [activeTab, setActiveTab] = useState<Tab>("lecture");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [result, setResult] = useState<RunResponse | SubmitResponse | null>(null);
  const { data: taskData, loading, submitting, error, submit, run } = useTask(lecture.id);

  // Esc — закрыть модалку (подсказка показывается в шапке).
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const problems = taskData?.problems ?? [];
  const selectedIndex = problems.findIndex((p) => p.id === selectedId);
  const selectedProblem = selectedIndex >= 0 ? problems[selectedIndex] : null;
  const solvedCount = problems.filter((p) => p.solved).length;

  // «Задачи»: если ни одна не выбрана — открываем первую нерешённую.
  useEffect(() => {
    if (activeTab === "tasks" && selectedId === null && problems.length > 0) {
      const target =
        problems.find((p) => !p.solved) ?? problems[0];
      setSelectedId(target.id);
    }
  }, [activeTab, selectedId, problems]);

  // Смена лекции (кнопка «Дальше») — сбрасываем выбор задачи и вердикт.
  useEffect(() => {
    setSelectedId(null);
    setResult(null);
    setActiveTab("lecture");
  }, [lecture.id]);

  const handleRun = async (code: string) => {
    if (!selectedProblem) return;
    try {
      setResult(await run(selectedProblem.id, code));
    } catch {
      // ошибка уже показана в ErrorBanner (useTask)
    }
  };

  const handleSubmit = async (code: string) => {
    if (!selectedProblem) return;
    try {
      const res = await submit(selectedProblem.id, code);
      setResult(res);
      onTaskStatusChange?.(lecture.id, res.task_status);
    } catch {
      // ошибка уже показана в ErrorBanner (useTask)
    }
  };
const problemCount = problems.length;
  const allSolved = problemCount > 0 && solvedCount === problemCount;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-100/50 backdrop-blur-sm p-2 sm:p-4 animate-fadeIn">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-7xl max-h-[94vh] flex flex-col shadow-xl overflow-hidden">

        {/* Modal Header */}
        <div className="flex items-center justify-between px-5 py-3.5 bg-slate-50 border-b border-slate-200 gap-3">
          <div className="flex items-center gap-3 min-w-0">
            <span className="bg-indigo-500/20 text-indigo-600 font-mono text-xs px-2.5 py-1 rounded-lg border border-indigo-500/30 shrink-0">
              Тема #{lecture.id}
            </span>
            <h2 className="text-lg font-bold text-white truncate">{lecture.name}</h2>
            {allSolved && (
              <span className="hidden md:inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-400 bg-emerald-500/15 px-2 py-0.5 rounded-full border border-emerald-500/30 shrink-0">
                <CheckCircle2 className="h-3 w-3" />
                Все задачи решены
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="hidden sm:inline text-[10px] text-slate-500">
              Esc — закрыть
            </span>
            <button
              onClick={onClose}
              aria-label="Закрыть"
              className="text-slate-500 hover:text-slate-900 p-2 rounded-lg hover:bg-slate-100 transition cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tabs Bar */}
        <div className="flex border-b border-slate-200 bg-slate-50 px-5 gap-4">
          <button
            onClick={() => setActiveTab("lecture")}
            className={`flex items-center gap-2 py-3 px-4 font-medium text-sm border-b-2 transition cursor-pointer ${
              activeTab === "lecture"
                ? "border-indigo-600 text-indigo-600"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <BookOpen className="w-4 h-4" />
            Лекция и Теория
          </button>
          <button
            onClick={() => setActiveTab("tasks")}
            className={`flex items-center gap-2 py-3 px-4 font-medium text-sm border-b-2 transition cursor-pointer ${
              activeTab === "tasks"
                ? "border-indigo-600 text-indigo-600"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            <Code className="w-4 h-4" />
            Практические задания {problemCount ? `(${problemCount})` : ""}
          </button>
        </div>
{/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-5 text-slate-300">
          {loading ? (
            <LoadingSpinner label="Загружаем материалы темы..." />
          ) : error ? (
            <ErrorBanner message={`Ошибка загрузки: ${error}`} compact />
          ) : activeTab === "lecture" ? (
            <LectureView lecture={taskData?.lecture_md ?? ""} taskId={lecture.id} />
          ) : selectedProblem ? (
            <ProblemWorkbench
              key={selectedProblem.id}
              problem={selectedProblem}
              index={selectedIndex}
              total={problems.length}
              lectureName={lecture.name}
              submitting={submitting}
              result={result}
              onRun={handleRun}
              onSubmit={handleSubmit}
              onPrev={selectedIndex > 0 ? () => setSelectedId(problems[selectedIndex - 1].id) : null}
              onNext={selectedIndex < problems.length - 1 ? () => setSelectedId(problems[selectedIndex + 1].id) : null}
              onBack={() => setSelectedId(null)}
            />
          ) : problemCount > 0 ? (
            <div className="space-y-4">
              <div className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/50 px-4 py-3">
                <div className="flex items-center gap-2 text-sm">
                  <ListChecks className="h-4 w-4 text-indigo-500" />
                  <span className="text-slate-300">
                    Решено задач: <span className="font-semibold text-white">{solvedCount}</span> из {problemCount}
                  </span>
                </div>
                <div className="w-40 h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full transition-all duration-500"
                    style={{ width: `${problemCount ? Math.round((solvedCount / problemCount) * 100) : 0}%` }}
                  />
                </div>
                <span className="ml-auto text-[10px] text-slate-500">
                  Выберите задачу, чтобы открыть воркбенч
                </span>
              </div>

              <ul className="space-y-2.5">
                {problems.map((problem, idx) => (
                  <li key={problem.id}>
                    <button
                      onClick={() => setSelectedId(problem.id)}
                      className="group w-full flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-left transition hover:border-indigo-500 hover:bg-slate-50 cursor-pointer"
                    >
                      <span className="text-xs font-mono bg-indigo-100 text-indigo-700 px-2 py-1 rounded-md border border-indigo-200 shrink-0">
                        №{idx + 1}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className="block text-sm font-semibold text-slate-900 truncate group-hover:text-indigo-700 transition">
                          {problem.title}
                        </span>
                        <span className="block text-[10px] font-mono text-slate-600 truncate">
                          {problem.entry_function ? `def ${problem.entry_function}(...)` : "реализуйте решение"}{" "}
                          • {problem.test_case_count} тест(а/ов)
                        </span>
                      </span>
                      {problem.solved && (
                        <span className="flex items-center gap-1 text-[10px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full border border-emerald-300 shrink-0">
                          <CheckCircle2 className="h-3 w-3" />
                          Решено
                        </span>
                      )}
                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded-full shrink-0 ${
                          problem.difficulty === "easy"
                            ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                            : problem.difficulty === "medium"
                              ? "bg-slate-100 text-slate-800 border border-slate-300"
                              : "bg-red-100 text-red-800 border border-red-300"
                        }`}
                      >
                        {problem.difficulty}
                      </span>
                      <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-700 group-hover:translate-x-1 transition shrink-0" />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p className="text-slate-400 italic">Задания для этой темы в разработке.</p>
          )}
        </div>
{/* Modal Footer */}
        <div className="flex items-center justify-between gap-3 px-5 py-3.5 bg-slate-50 border-t border-slate-200">
          <p className="text-[10px] text-slate-500 hidden lg:block">
            ПКМ по карточке на роадмапе — быстро сменить статус темы
          </p>
          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={onClose}
              className="bg-slate-100 hover:bg-slate-200 text-slate-800 px-5 py-2 rounded-xl text-sm font-medium transition cursor-pointer"
            >
              Закрыть
            </button>
            {nextLecture && onOpenLecture && (
              <button
                onClick={() => onOpenLecture(nextLecture)}
                className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-400 text-white px-5 py-2 rounded-xl text-sm font-semibold transition cursor-pointer"
                title={`Следующая тема: ${nextLecture.name}`}
              >
                Следующая тема
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}