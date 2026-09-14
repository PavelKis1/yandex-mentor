import { useCallback, useEffect, useState } from "react";
import { fetchLecture, runProblem, submitProblem } from "../api/client";
import type { LectureData, RunResponse, SubmitResponse } from "../types";
import { errorMessage } from "../utils/errors";

interface UseTask {
  data: LectureData | null;
  loading: boolean;
  submitting: boolean;
  error: string | null;
  /** Отправка решения на сервер: сохраняет код и возвращает результат ревью. */
  submit: (problemId: string, code: string) => Promise<SubmitResponse>;
  run: (problemId: string, code: string) => Promise<RunResponse>;
}

/** Загрузка полных данных темы (лекция + задания + код решения). */
export function useTask(lectureId: string | null): UseTask {
  const [data, setData] = useState<LectureData | null>(null);
  const [loadedLectureId, setLoadedLectureId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // loading = задача ещё не загружена или запрос для нового id в полёте.
  const loading = lectureId !== null && lectureId !== loadedLectureId;

  useEffect(() => {
    if (!lectureId) return;
    let cancelled = false;

    fetchLecture(lectureId)
      .then((fetched) => {
        if (!cancelled) {
          setData(fetched);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(errorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoadedLectureId(lectureId);
      });

    return () => {
      cancelled = true;
    };
  }, [lectureId]);

  const submit = useCallback(
    async (problemId: string, code: string): Promise<SubmitResponse> => {
      setSubmitting(true);
      setError(null);
      try {
        const res = await submitProblem(problemId, code);
        // актуализируем код решения и статус «решено» в загруженных данных
        setData((prev) =>
          prev
            ? {
                ...prev,
                problems: prev.problems.map((p) =>
                  p.id === problemId
                    ? { ...p, code, solved: res.verdict === "accepted" ? true : p.solved }
                    : p
                ),
              }
            : prev
        );
        return res;
      } catch (err) {
        setError(errorMessage(err));
        throw err;
      } finally {
        setSubmitting(false);
      }
    },
    [],
  );

  const run = useCallback(
    async (problemId: string, code: string): Promise<RunResponse> => {
      setSubmitting(true);
      setError(null);
      try {
        return await runProblem(problemId, code);
      } catch (err) {
        setError(errorMessage(err));
        throw err;
      } finally {
        setSubmitting(false);
      }
    },
    [],
  );

  return { data, loading, submitting, error, submit, run };
}
