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
  const completedCount = stageLectures.filter((lec) => progress[lec.id] === "done").length;
  const stageProgress = stageLectures.length
    ? Math.round((completedCount / stageLectures.length) * 100)
    : 0;

  return (
    <div className="space-y-6">
      {/* Interactive Module Tab-Card */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-white border border-slate-200 p-6 rounded-3xl gap-4 shadow-sm hover:border-indigo-200 transition-all duration-300">
        <div className="flex items-center gap-4">
          <div className="text-3xl bg-indigo-50 p-4 rounded-2xl border border-indigo-100 text-indigo-600">
            {stage.icon}
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-950">
              {stage.name}
            </h2>
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
        </div>
      </div>

      {/* Stage Lectures Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
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
  );
}

