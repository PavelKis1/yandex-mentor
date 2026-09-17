import { LectureChapters } from "./LectureChapters";
import type { LectureData } from "../types";

interface LectureViewProps {
  lecture?: string | null;
  /** Идентификатор темы — ключ для чтения позиции в localStorage. */
  taskId?: string;
  /** Метаданные лекции — опционально, для шапки/шпаргалки/привязанных задач. */
  meta?: LectureData | null;
  onOpenTask?: (taskId: string, lectureId: string) => void;
}

export function LectureView({ lecture, taskId, meta, onOpenTask }: LectureViewProps) {
  if (!lecture || lecture.trim().length === 0) {
    return (
      <p className="text-slate-400 italic">Лекция для данной темы готовится.</p>
    );
  }

  return (
    <LectureChapters
      markdown={lecture}
      taskId={taskId}
      meta={meta}
      onOpenTask={onOpenTask}
    />
  );
}