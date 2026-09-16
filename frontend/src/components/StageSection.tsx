import { useState } from "react";
import { ChevronDown } from "lucide-react";
import type { ProgressMap, RoadmapStage, TaskStatus, TaskSummary } from "../types";
import { TaskCard } from "./TaskCard";

interface StageSectionProps {
  stage: RoadmapStage;
  stageIndex: number;
  progress: ProgressMap;
  onSelectTask: (task: TaskSummary) => void;
  onSetStatus?: (lectureId: string, status: TaskStatus) => void;
}

export function StageSection({
  stage,
  stageIndex,
  progress,
  onSelectTask,
  onSetStatus,
}: StageSectionProps) {
  const stageLectures = stage.lectures ?? [];
  // Модули свернуты по умолчанию — темы раскрываются по клику на заголовок.
  const [open, setOpen] = useState(false);
  const completedCount = stageLectures.filter((lec) => progress[lec.id] === "done").length;
  const stageProgress = stageLectures.length
    ? Math.round((completedCount / stageLectures.length) * 100)
    : 0;

  return (
    <div className="space-y-6">
      {/* Заголовок модуля: кликабельная «шапка», раскрывающая список тем */}
      <button
        type="button"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
        className="group flex w-full flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-3xl border border-slate-200 bg-white p-6 text-left shadow-sm transition-all duration-300 hover:border-indigo-200 cursor-pointer"
      >
        <div className="flex items-center gap-4">
          <div className="text-3xl bg-indigo-50 p-4 rounded-2xl border border-indigo-100 text-indigo-600">
            {stage.icon}
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-950">{stage.name}</h2>
            <p className="text-sm text-slate-500 font-medium">
              Модуль {stageIndex + 1} &bull; {completedCount} / {stageLectures.length} тем завершено
            </p>
          </div>
        </div>

        <div className="w-full sm:w-auto flex items-center gap-4">
          <div className="flex-1 sm:w-48 h-3 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
            <div
              className="bg-indigo-600 h-full rounded-full transition-all duration-500"
              style={{ width: `${stageProgress}%` }}
            ></div>
          </div>
          <span className="text-sm font-bold text-indigo-700 w-12 text-right">
            {stageProgress}%
          </span>
          <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-slate-500 transition-all duration-300 group-hover:border-indigo-200 group-hover:text-indigo-600">
            <ChevronDown
              className={`h-5 w-5 transition-transform duration-300 ${open ? "rotate-180" : ""}`}
            />
          </span>
        </div>
      </button>

      {/* Сворачиваемый контент: плавная анимация высоты через grid-template-rows без сторонних библиотек */}
      <div
        className={`grid transition-[grid-template-rows] duration-500 ease-in-out ${
          open ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
        }`}
      >
        <div className="overflow-hidden min-h-0">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 pt-2">
            {stageLectures.map((lecture) => (
              <TaskCard
                key={lecture.id}
                task={lecture}
                status={progress[lecture.id] ?? "todo"}
                onSelect={onSelectTask}
                onSetStatus={onSetStatus}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

