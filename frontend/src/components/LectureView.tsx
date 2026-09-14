import { LectureChapters } from "./LectureChapters";

interface LectureViewProps {
  lecture?: string | null;
  /** Идентификатор темы — ключ для чтения позиции в localStorage. */
  taskId?: string;
}

export function LectureView({ lecture, taskId }: LectureViewProps) {
  if (!lecture || lecture.trim().length === 0) {
    return (
      <p className="text-slate-400 italic">Лекция для данной темы готовится.</p>
    );
  }

  return <LectureChapters markdown={lecture} taskId={taskId} />;
}