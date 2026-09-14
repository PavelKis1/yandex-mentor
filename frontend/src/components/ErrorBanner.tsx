import { AlertCircle } from "lucide-react";

interface ErrorBannerProps {
  message: string;
  title?: string;
  /** Компактный вариант для вложенных блоков (модалка). */
  compact?: boolean;
}

export function ErrorBanner({
  message,
  title = "Не удалось подключиться к бэкенду",
  compact = false,
}: ErrorBannerProps) {
  const containerClass = compact
    ? "bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl flex items-center gap-3"
    : "bg-red-500/10 border border-red-500/30 text-red-400 p-6 rounded-2xl flex items-center gap-4 max-w-xl mx-auto my-12 shadow-xl";

  return (
    <div className={containerClass}>
      <AlertCircle className={`shrink-0 text-red-500 ${compact ? "w-5 h-5" : "w-8 h-8"}`} />
      <div>
        {!compact && <h3 className="font-bold text-white mb-1">{title}</h3>}
        <p className="text-sm text-red-300">{message}</p>
      </div>
    </div>
  );
}