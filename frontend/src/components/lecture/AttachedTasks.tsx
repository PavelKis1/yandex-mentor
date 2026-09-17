import { ArrowRight } from "lucide-react";
import type { InternalTaskRef, ProblemPublic } from "../../types";

interface AttachedTasksProps {
  tasks: InternalTaskRef[];
  /** Задачи лекции с per-task флагом `solved` — источник прогресса выполнения. */
  problems: ProblemPublic[];
  onOpenTask: (taskId: string, lectureId: string) => void;
}

export function AttachedTasks({ tasks, problems, onOpenTask }: AttachedTasksProps) {
  if (!tasks || tasks.length === 0) return null;

  // Сопоставляем привязанные задачи (taskId, напр. «01-p1») со статусом из problems (p.id).
  const solvedByTask = new Map(problems.map((p) => [p.id, Boolean(p.solved)]));
  const total = tasks.length;
  const solved = tasks.filter((t) => solvedByTask.get(t.taskId)).length;
  const percent = Math.round((solved / total) * 100);

  return (
    <div className="mt-8">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h2 className="text-xl font-bold">Закрепить на практике</h2>
        <span className="text-sm font-medium text-slate-600">
          {solved} из {total} решено · {percent}%
        </span>
      </div>

      <div
        role="progressbar"
        aria-valuenow={percent}
        aria-valuemin={0}
        aria-valuemax={100}
        className="mb-5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100 border border-slate-200"
      >
        <div
          className="h-full rounded-full bg-indigo-500 transition-all duration-300"
          style={{ width: `${percent}%` }}
        />
      </div>

      <div className="grid gap-3">
        {tasks.map(task => {
          const done = solvedByTask.get(task.taskId) === true;
          const lectureId = task.lectureId ?? task.taskId.split("-")[0];

          return (
            <button
              key={task.taskId}
              onClick={() => onOpenTask(task.taskId, lectureId)}
              className="flex items-center justify-between p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition text-left"
            >
              <div className="flex items-center gap-3">
                 <span className={`w-3 h-3 rounded-full ${done ? 'bg-emerald-500' : 'bg-slate-300'}`} />
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
