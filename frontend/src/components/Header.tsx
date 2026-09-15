import { RefreshCw, Terminal, UserCircle } from "lucide-react";

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
        <div className="flex items-center gap-4">
          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-md"
            title="Обновить прогресс"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span className="text-sm font-semibold">Синхронизировать</span>
          </button>
          
          <div className="h-8 w-px bg-slate-200 mx-2" />

          <div className="flex items-center gap-2 text-slate-400">
            <UserCircle className="w-9 h-9" />
          </div>
        </div>

      </div>
    </header>
  );
}
