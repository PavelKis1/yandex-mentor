import Editor from "@monaco-editor/react";
import { useCallback, useEffect, useState } from "react";
import type { ProblemPublic, RunResponse, SubmitResponse } from "../types";
import { readJson, readText, writeJson, writeText } from "../utils/storage";

interface SolutionEditorProps {
  problem: ProblemPublic;
  submitting: boolean;
  result: RunResponse | SubmitResponse | null;
  onRun: (code: string) => void;
  onSubmit: (code: string) => void;
}

export function SolutionEditor({
  problem,
  submitting,
  result: propResult,
  onRun,
  onSubmit,
}: SolutionEditorProps) {
  const [resetKey, setResetKey] = useState(0);
  const STORAGE_KEY = `solution:${problem.id}`;
  const RESULT_KEY = `result:${problem.id}`;
  
  const [code, setCode] = useState(() => readText(STORAGE_KEY) ?? problem.starter_code ?? "");
  const [localResult, setLocalResult] = useState<RunResponse | SubmitResponse | null>(() => readJson<RunResponse | SubmitResponse>(RESULT_KEY));

  useEffect(() => {
    writeText(STORAGE_KEY, code);
  }, [code, STORAGE_KEY]);

  useEffect(() => {
    if (propResult) {
      setLocalResult(propResult);
      writeJson(RESULT_KEY, propResult);
    }
  }, [propResult, RESULT_KEY]);

  const handleReset = useCallback(() => {
    const defaultCode = problem.starter_code ?? "";
    setCode(defaultCode);
    setLocalResult(null);
    writeText(STORAGE_KEY, defaultCode);
    writeJson(RESULT_KEY, null);
    setResetKey(prev => prev + 1);
  }, [problem.starter_code, STORAGE_KEY, RESULT_KEY]);

  const result = propResult ?? localResult;

  return (
    <div className="flex flex-col h-full gap-2">
      <div className="flex justify-between p-2 bg-white rounded-lg border border-slate-200">
        <button 
            onClick={handleReset} 
            className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-sm transition cursor-pointer"
        >
          Сбросить
        </button>
        <div className="flex gap-2">
          <button 
            onClick={() => onRun(code)} 
            disabled={submitting} 
            className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded text-sm transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {submitting ? "Запуск..." : "Запустить"}
          </button>
          <button 
            onClick={() => onSubmit(code)} 
            disabled={submitting} 
            className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-sm transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {submitting ? "Отправка..." : "Отправить"}
          </button>
        </div>
      </div>
      <Editor
        key={resetKey}
        height="300px"
        value={code}
        onChange={(v) => setCode(v ?? "")}
        theme="vs-light"
        options={{
            minimap: { enabled: false },
            fontSize: 14,
            padding: { top: 10 }
        }}
      />
      
      {/* Result Display */}
      {result && (
        <div className="p-3 bg-white border border-slate-200 rounded-lg text-sm">
            <div className={`font-bold mb-2 ${result.verdict === 'accepted' ? 'text-emerald-600' : 'text-red-600'}`}>
                Вердикт: {result.verdict}
            </div>
            {result.results.map((r, i) => (
                <div key={i} className="text-xs text-slate-700 font-mono">
                    Тест {i + 1}: {r.passed ? "✅ Пройден" : `❌ Ошибка: ${r.error || "Неверный ответ"}`}
                </div>
            ))}
            <div className="text-xs text-slate-500 mt-2">Время: {result.time_ms} мс</div>
        </div>
      )}
    </div>
  );
}
