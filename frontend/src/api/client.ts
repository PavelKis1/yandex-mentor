import { API_BASE } from "../config";
import type {
  LectureData,
  ProgressMap,
  RoadmapResponse,
  RunResponse,
  SubmitResponse,
  TaskStatus,
  ProblemPublic,
} from "../types";

async function getJson<T>(path: string, init?: RequestInit): Promise<T> {
  const { headers: initHeaders, ...restInit } = init || {};
  const headers = new Headers(initHeaders);
  headers.set("Authorization", "Basic YWRtaW46YWRtaW4=");
  
  const url = `${API_BASE}${path}`;
  console.log(`[API Request] ${restInit.method ?? 'GET'} ${url}`, { headers: Object.fromEntries(headers.entries()) });
  
  const res = await fetch(url, { ...restInit, headers });
  
  if (!res.ok) {
    console.error(`[API Error] ${res.status} ${res.statusText}`);
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}

export function fetchRoadmap(): Promise<RoadmapResponse> {
  return getJson<RoadmapResponse>("/api/roadmap");
}

export function fetchProgress(): Promise<ProgressMap> {
  return getJson<ProgressMap>("/api/progress");
}

export function fetchLecture(lectureId: string): Promise<LectureData> {
  return getJson<LectureData>(`/api/lectures/${lectureId}`);
}

export function fetchProblem(problemId: string): Promise<ProblemPublic> {
  return getJson<ProblemPublic>(`/api/tasks/${problemId}`);
}

export function runProblem(problemId: string, code: string): Promise<RunResponse> {
  return getJson<RunResponse>(`/api/tasks/${problemId}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
}

export function submitProblem(problemId: string, code: string): Promise<SubmitResponse> {
  return getJson<SubmitResponse>(`/api/tasks/${problemId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
}

export function saveProblemCode(problemId: string, code: string): Promise<{ status: string }> {
  return getJson<{ status: string }>(`/api/tasks/${problemId}/code`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
}

export function setTaskStatus(
  lectureId: string,
  status: TaskStatus,
): Promise<{ task_id: string; status: TaskStatus }> {
  return getJson<{ task_id: string; status: TaskStatus }>(`/api/task/${lectureId}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
}
