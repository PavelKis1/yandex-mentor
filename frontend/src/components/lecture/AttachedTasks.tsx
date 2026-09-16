import { ArrowRight } from "lucide-react";
import type { InternalTaskRef, TaskStatus } from "../../types";

interface AttachedTasksProps {
  tasks: InternalTaskRef[];
  progress: Record<string, TaskStatus>;
  onOpenTask: (taskId: string, lectureId: string) => void;
}

export function AttachedTasks({ tasks, progress, onOpenTask }: AttachedTasksProps) {
  if (!tasks || tasks.length === 0) return null;

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">Закрепить на практике</h2>
      <div className="grid gap-3">
        {tasks.map(task => {
          const status = progress[task.lectureId ?? ""] ?? "todo";
          const lectureId = task.lectureId ?? task.taskId.split("-")[0];

          return (
            <button
              key={task.taskId}
              onClick={() => onOpenTask(task.taskId, lectureId)}
              className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition text-left"
            >
              <div className="flex items-center gap-3">
                 <span className={`w-3 h-3 rounded-full ${status === 'done' ? 'bg-emerald-500' : status === 'wip' ? 'bg-amber-400' : 'bg-slate-300'}`} />
                 <span className="font-medium text-slate-800">{task.title}</span>
                 {task.difficulty && <span className="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded">{task.difficulty}</span>}
              </div>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
