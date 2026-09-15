interface ReadingProgressBarProps {
  /** Доля прочитанного от 0 до 1. */
  value: number;
}

/** Тонкий индикатор прогресса чтения лекции (главы / прокрутка). */
export function ReadingProgressBar({ value }: ReadingProgressBarProps) {
  const percent = Math.max(0, Math.min(100, Math.round(value * 100)));

  return (
    <div
      role="progressbar"
      aria-valuenow={percent}
      aria-valuemin={0}
      aria-valuemax={100}
      className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 border border-slate-200"
    >
      <div
        className="h-full rounded-full bg-indigo-500 transition-all duration-300"
        style={{ width: `${percent}%` }}
      />
    </div>
  );
}