import { useMemo, useState } from "react";
import { ErrorBanner } from "./components/ErrorBanner";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { RoadmapView } from "./components/RoadmapView";
import { TopicModal } from "./components/TopicModal";
import { useRoadmap } from "./hooks/useRoadmap";
import type { TaskSummary } from "./types";

export default function App() {
  const {
    roadmap,
    progress,
    completedTasks,
    loading,
    error,
    handleRefresh,
    setTaskStatus,
    updateTaskStatus,
  } = useRoadmap();
  const [selectedTask, setSelectedTask] = useState<TaskSummary | null>(null);
  // Deep-link: задача темы, которую нужно открыть после загрузки модалки.
  const [pendingProblemId, setPendingProblemId] = useState<string | null>(null);

  // Следующая тема по порядку (для кнопки «Дальше» в модалке).
  const allLectures = useMemo(
    () => roadmap.flatMap((stage) => stage.lectures ?? []),
    [roadmap],
  );
  const selectedIndex = selectedTask
    ? allLectures.findIndex((lecture) => lecture.id === selectedTask.id)
    : -1;
  const nextLecture =
    selectedIndex >= 0 && selectedIndex < allLectures.length - 1
      ? allLectures[selectedIndex + 1]
      : null;
  const prevLecture = selectedIndex > 0 ? allLectures[selectedIndex - 1] : null;

  /** Навигация между темами — сбрасываем deep-link, чтобы не «залипала» задача. */
  const openLecture = (lecture: TaskSummary) => {
    setPendingProblemId(null);
    setSelectedTask(lecture);
  };

  /** Deep-link из блока «Закрепить на практике»: открыть тему и конкретную задачу. */
  const handleOpenTask = (taskId: string, lectureId: string) => {
    const target = allLectures.find((l) => l.id === lectureId);
    if (!target) return;
    setSelectedTask(target);
    setPendingProblemId(taskId);
  };

  const closeModal = () => {
    setPendingProblemId(null);
    setSelectedTask(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-indigo-200 selection:text-slate-900">

      <Header
        onRefresh={handleRefresh}
        loading={loading}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {error ? (
          <ErrorBanner message={error} />
        ) : (
          <RoadmapView
            roadmap={roadmap}
            progress={progress}
            completedTasks={completedTasks}
            onSelectTask={setSelectedTask}
            onSetStatus={updateTaskStatus}
          />
        )}
      </main>

      <Footer />

      {selectedTask && (
        <TopicModal
          key={selectedTask.id}
          lecture={selectedTask}
          nextLecture={nextLecture}
          prevLecture={prevLecture}
          onOpenLecture={openLecture}
          onClose={closeModal}
          onTaskStatusChange={setTaskStatus}
          progress={progress}
          initialProblemId={pendingProblemId}
          onOpenTask={handleOpenTask}
        />
      )}

    </div>
  );
}