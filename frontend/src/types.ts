/* Типы данных API — зеркало src/models.py и src/api/routes.py бэкенда. */

export type TaskStatus = "todo" | "wip" | "done";
export type ProgressMap = Record<string, TaskStatus>;

export interface TaskSummary {
  id: string;
  name: string;
}

export interface RoadmapStage {
  id: string;
  name: string;
  icon: string;
  lectures: TaskSummary[];
}

export interface RoadmapResponse {
  roadmap: RoadmapStage[];
  total: number;
}

export type Difficulty = "easy" | "medium" | "hard";

export interface ProblemPublic {
  id: string;
  title: string;
  difficulty: Difficulty;
  order: number;
  description: string;
  examples: any[];
  constraints: string[];
  hints: string[];
  starter_code: string;
  entry_function: string | null;
  code: string | null; // сохранённое решение пользователя
  test_case_count: number;
  solved?: boolean;
}

export interface LectureData {
  id: string;
  name: string;
  stage_id: string;
  stage_name: string;
  lecture_md: string;
  status: TaskStatus;
  problems: ProblemPublic[];
}

export type Verdict =
  | "accepted"
  | "wrong_answer"
  | "runtime_error"
  | "timeout"
  | "syntax_error"
  | "no_tests";

export interface TestCaseResult {
  id: string;
  passed: boolean;
  expected: any;
  actual: any;
  error?: string | null;
}

export interface RunResponse {
  problem_id: string;
  verdict: Verdict;
  results: TestCaseResult[];
  time_ms: number;
}

export interface SubmitResponse extends RunResponse {
  task_status: TaskStatus;
  lecture_id: string;
}
