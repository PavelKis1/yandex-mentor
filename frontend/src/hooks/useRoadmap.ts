import { useCallback, useEffect, useState } from "react";
import { fetchProgress, fetchRoadmap, setTaskStatus as setTaskStatusRemote } from "../api/client";
import type { ProgressMap, RoadmapStage, TaskStatus } from "../types";
import { errorMessage } from "../utils/errors";
import { getCache, setCache } from "../utils/cache";

const CACHE_KEY = "roadmap";

const DEFAULT_TOTAL = 69;

interface RoadmapSnapshot {
  roadmap: RoadmapStage[];
  total: number;
  progress: ProgressMap;
}

/** Чистая загрузка данных (без состояния) — используется и эффектом, и refresh. */
async function fetchRoadmapData(): Promise<RoadmapSnapshot> {
  const [roadmapRes, progressRes] = await Promise.all([fetchRoadmap(), fetchProgress()]);
  const data = {
    roadmap: roadmapRes.roadmap ?? [],
    total: roadmapRes.total ?? DEFAULT_TOTAL,
    progress: progressRes,
  };
  setCache(CACHE_KEY, data);
  return data;
}

interface UseRoadmap {
  roadmap: RoadmapStage[];
  progress: ProgressMap;
  totalTasks: number;
  completedTasks: number;
  loading: boolean;
  error: string | null;
  /** Перезапуск сканирования ментором + перезагрузка данных. */
  handleRefresh: () => Promise<void>;
  /** Локальное обновление статуса одной темы (без полного сканирования). */
  setTaskStatus: (taskId: string, status: TaskStatus) => void;
  /** Оptimistic-смена статуса с записью на сервер (POST /api/task/{id}/status). */
  updateTaskStatus: (taskId: string, status: TaskStatus) => void;
}

/** Единый источник данных роадмапа: состояние, загрузка, refresh, счётчики. */
export function useRoadmap(): UseRoadmap {
  const [roadmap, setRoadmap] = useState<RoadmapStage[]>([]);
  const [progress, setProgress] = useState<ProgressMap>({});
  const [totalTasks, setTotalTasks] = useState(DEFAULT_TOTAL);
  const [loaded, setLoaded] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 1. Попытка загрузить из кэша
    const cached = getCache<RoadmapSnapshot>(CACHE_KEY);
    if (cached) {
      setRoadmap(cached.roadmap);
      setTotalTasks(cached.total);
      setProgress(cached.progress);
      setLoaded(true);
    }

    let cancelled = false;
    fetchRoadmapData()
      .then((data) => {
        if (cancelled) return;
        setRoadmap(data.roadmap);
        setTotalTasks(data.total);
        setProgress(data.progress);
      })
      .catch((err) => {
        if (!cancelled) setError(errorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoaded(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      // Просто перечитываем статусы с сервера: прогресс ведёт бэкенд
      // (submit'ы и ручные смены статусов), а сканирования файлов нет.
      const data = await fetchRoadmapData();
      setRoadmap(data.roadmap);
      setTotalTasks(data.total);
      setProgress(data.progress);
      setError(null);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setRefreshing(false);
    }
  }, []);

  const completedTasks = Object.values(progress).filter((value) => value === "done").length;

  const setTaskStatus = useCallback((taskId: string, status: TaskStatus) => {
    setProgress((prev) => ({ ...prev, [taskId]: status }));
  }, []);

  // ПКМ по карточке: обновляем UI сразу, на сервер уходит фоновая запись.
  const updateTaskStatus = useCallback((taskId: string, status: TaskStatus) => {
    setProgress((prev) => ({ ...prev, [taskId]: status }));
    setTaskStatusRemote(taskId, status).catch((err) => setError(errorMessage(err)));
  }, []);

  return {
    roadmap,
    progress,
    totalTasks,
    completedTasks,
    loading: !loaded || refreshing,
    error,
    handleRefresh,
    setTaskStatus,
    updateTaskStatus,
  };
}