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
    <div className="space-y-4">

      {/* Stage Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between bg-slate-900/90 border border-slate-800 p-5 rounded-2xl gap-3 shadow-lg">
        <div className="flex items-center gap-3">
          <span className="text-3xl bg-slate-800 p-2.5 rounded-xl border border-slate-700 shadow-inner">
            {stage.icon}
          </span>
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              Этап {stageIndex + 1}: {stage.name}
            </h2>
            <p className="text-xs text-slate-400">
              {stageLectures.length} тем в разделе
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-xs text-slate-400 text-right">
            <div>Пройдено: {completedCount} из {stageLectures.length}</div>
          </div>
          <div className="w-28 bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700">
            <div
              className="bg-amber-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${stageProgress}%` }}
            ></div>
          </div>
          <span className="text-xs font-semibold text-amber-400 w-10 text-right">
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