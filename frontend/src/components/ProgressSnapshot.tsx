import { Award, CheckCircle2 } from "lucide-react";
import type { ProgressMap, RoadmapStage } from "../types";

interface ProgressSnapshotProps {
  roadmap: RoadmapStage[];
  progress: ProgressMap;
  completedTasks: number;
}

/** Сводка прогресса обучения: итог + мини-полоски по разделам. */
export function ProgressSnapshot({ roadmap, progress, completedTasks }: ProgressSnapshotProps) {
  const total = roadmap.reduce((sum, stage) => sum + (stage.lectures?.length ?? 0), 0);
  if (total === 0) return null;

  const percent = Math.round((completedTasks / total) * 100);

  return (
    <div className="glass-card p-5 mb-10">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <span className="bg-amber-500/15 border border-amber-500/25 p-2.5 rounded-xl text-amber-400">
            <Award className="w-5 h-5" />
          </span>
          <div>
            <h2 className="font-semibold text-white leading-tight">Ваш прогресс</h2>
            <p className="text-xs text-slate-400 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Пройдено {completedTasks} из {total} тем
            </p>
          </div>
        </div>
        <div className="text-right">
          <span className="text-3xl font-bold text-amber-400">{percent}%</span>
          <span className="block text-[10px] text-slate-500 uppercase tracking-wider">обучения</span>
        </div>
      </div>

      {/* Общая полоса прогресса */}
      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-indigo-500 transition-all duration-500"
          style={{ width: `${percent}%` }}
        />
      </div>

      {/* Мини-полоски по этапам */}
      <div className="mt-4 flex flex-wrap gap-3">
        {roadmap.map((stage) => {
          const stageLectures = stage.lectures ?? [];
          const done = stageLectures.filter((lecture) => progress[lecture.id] === "done").length;
          const stagePercent = stageLectures.length
            ? Math.round((done / stageLectures.length) * 100)
            : 0;
          return (
            <div key={stage.id} className="min-w-[110px] flex-1">
              <div className="mb-1 flex items-center justify-between gap-2 text-[10px] text-slate-400">
                <span className="flex items-center gap-1 truncate">
                  <span className="text-sm leading-none">{stage.icon}</span>
                  <span className="truncate">{stage.name}</span>
                </span>
                <span className="shrink-0">
                  {done}/{stageLectures.length}
                </span>
              </div>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-800/80">
                <div
                  className="h-full rounded-full bg-amber-500/70 transition-all duration-500"
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