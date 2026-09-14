import type { ProgressMap, RoadmapStage, TaskStatus, TaskSummary } from "../types";
import { ProgressSnapshot } from "./ProgressSnapshot";
import { StageSection } from "./StageSection";

interface RoadmapViewProps {
  roadmap: RoadmapStage[];
  progress: ProgressMap;
  completedTasks: number;
  onSelectTask: (task: TaskSummary) => void;
  onSetStatus?: (taskId: string, status: TaskStatus) => void;
}

export function RoadmapView({
  roadmap,
  progress,
  completedTasks,
  onSelectTask,
  onSetStatus,
}: RoadmapViewProps) {
  if (roadmap.length === 0) {
    return (
      <div className="flex justify-center items-center py-20 text-slate-400">
        Загрузка роадмапа...
      </div>
    );
  }

  return (
    <div className="space-y-12 pb-16">
      <ProgressSnapshot roadmap={roadmap} progress={progress} completedTasks={completedTasks} />

      {roadmap.map((stage, stageIndex) => (
        <StageSection
          key={stage.id}
          stage={stage}
          stageIndex={stageIndex}
          progress={progress}
          onSelectTask={onSelectTask}
          onSetStatus={onSetStatus}
        />
      ))}
    </div>
  );
}