import { RefreshCw, Terminal } from "lucide-react";

interface HeaderProps {
  onRefresh: () => void;
  loading: boolean;
}

export function Header({ onRefresh, loading }: HeaderProps) {
  return (
    <header className="bg-white border-b border-slate-200 text-slate-900 sticky top-0 z-30 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">

        {/* Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2.5 rounded-xl text-white shadow-md flex items-center justify-center">
            <Terminal className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-950">
              Yandex Backend Mentor
            </h1>
            <p className="text-xs text-slate-500">Платформа подготовки Middle/Senior Backend инженеров</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-6">
          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 hover:text-indigo-800 px-4 py-2 rounded-xl border border-indigo-200 transition-all active:scale-95 disabled:opacity-50 cursor-pointer hover:shadow-md"
            title="Обновить прогресс и запустить ментор"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span className="text-sm font-semibold">Синхронизировать</span>
          </button>
        </div>

      </div>
    </header>
  );
}
