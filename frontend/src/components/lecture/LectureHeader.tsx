import type { DifficultyLevel } from "../../types";

interface LectureHeaderProps {
  title: string;
  description?: string;
  durationMinutes?: number;
  difficulty?: DifficultyLevel;
  tags?: string[];
  learningOutcomes?: string[];
}

export function LectureHeader({
  title,
  description,
  durationMinutes,
  difficulty,
  tags,
  learningOutcomes,
}: LectureHeaderProps) {
  const difficultyColors = {
    junior: "bg-emerald-100 text-emerald-800 border-emerald-200",
    middle: "bg-blue-100 text-blue-800 border-blue-200",
    hard: "bg-red-100 text-red-800 border-red-200",
  };

  return (
    <header className="mb-8 border-b border-slate-200 pb-6">
      <h1 className="text-3xl font-bold text-slate-900 mb-4">{title}</h1>
      
      <div className="flex flex-wrap gap-4 text-sm text-slate-600 mb-4">
        {durationMinutes && (
          <span className="flex items-center gap-1.5">⏱️ {durationMinutes} мин</span>
        )}
        {difficulty && (
          <span className={`px-2.5 py-0.5 rounded-full border ${difficultyColors[difficulty]}`}>
            {difficulty.toUpperCase()}
          </span>
        )}
        {tags?.map(tag => (
          <span key={tag} className="bg-slate-100 px-2.5 py-0.5 rounded-full">#{tag}</span>
        ))}
      </div>

      {description && <p className="text-lg text-slate-700 mb-6">{description}</p>}

      {learningOutcomes && learningOutcomes.length > 0 && (
        <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4">
          <h3 className="font-semibold text-indigo-900 mb-2">🎯 Чему вы научитесь:</h3>
          <ul className="list-disc list-inside text-sm text-indigo-800 space-y-1">
            {learningOutcomes.map((item, i) => <li key={i}>{item}</li>)}
          </ul>
        </div>
      )}
    </header>
  );
}
