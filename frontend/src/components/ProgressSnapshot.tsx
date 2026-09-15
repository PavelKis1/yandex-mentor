import { Award, CheckCircle2 } from "lucide-react";
import type { ProgressMap, RoadmapStage } from "../types";

interface ProgressSnapshotProps {
  roadmap: RoadmapStage[];
  progress: ProgressMap;
  completedTasks: number;
}

/** Общая сводка прогресса обучения: итого + мини-полоски по модулям. */
export function ProgressSnapshot({ roadmap, progress, completedTasks }: ProgressSnapshotProps) {
  const total = roadmap.reduce((sum, stage) => sum + (stage.lectures?.length ?? 0), 0);
  if (total === 0) return null;

  const percent = Math.round((completedTasks / total) * 100);

  return (
    <div className="bg-white border border-slate-200 p-6 mb-10 rounded-3xl shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <span className="bg-amber-100 border border-amber-200 p-3 rounded-2xl text-amber-600">
            <Award className="w-6 h-6" />
          </span>
          <div>
            <h2 className="font-bold text-slate-950 text-lg leading-tight">Ваш прогресс</h2>
            <p className="text-sm text-slate-500 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Пройдено {completedTasks} из {total} тем
            </p>
          </div>
        </div>
        <div className="text-right">
          <span className="text-3xl font-bold text-indigo-600">{percent}%</span>
          <span className="block text-[10px] text-slate-400 uppercase tracking-wider font-medium">обучения</span>
        </div>
      </div>

      {/* Общая полоса прогресса */}
      <div className="mt-5 h-3 w-full overflow-hidden rounded-full bg-slate-100 border border-slate-200">
        <div
          className="h-full rounded-full bg-indigo-600 transition-all duration-700 ease-out"
          style={{ width: `${percent}%` }}
        />
      </div>

      {/* Мини-полоски по модулям */}
      <div className="mt-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {roadmap.map((stage) => {
          const stageLectures = stage.lectures ?? [];
          const done = stageLectures.filter((lecture) => progress[lecture.id] === "done").length;
          const stagePercent = stageLectures.length
            ? Math.round((done / stageLectures.length) * 100)
            : 0;
          return (
            <div key={stage.id} className="space-y-1.5">
              <div className="flex items-center justify-between gap-2 text-[11px] text-slate-500 font-medium">
                <span className="flex items-center gap-1.5 truncate">
                  <span className="text-sm leading-none">{stage.icon}</span>
                  <span className="truncate">{stage.name}</span>
                </span>
                <span className="shrink-0 text-slate-400">
                  {done}/{stageLectures.length}
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100 border border-slate-200">
                <div
                  className="h-full rounded-full bg-indigo-500 transition-all duration-700 ease-out"
                  style={{ width: `${stagePercent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
