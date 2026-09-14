import { Award, RefreshCw, Terminal } from "lucide-react";

interface HeaderProps {
  totalTasks: number;
  completedTasks: number;
  onRefresh: () => void;
  loading: boolean;
}

export function Header({ totalTasks, completedTasks, onRefresh, loading }: HeaderProps) {
  const percent = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <header className="bg-white border-b border-slate-200 text-slate-900 sticky top-0 z-30 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">

        {/* Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="bg-indigo-500 p-2 rounded-xl text-white font-bold shadow-md flex items-center justify-center">
            <Terminal className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-950">
              Yandex Backend Mentor
            </h1>
            <p className="text-xs text-slate-500">Платформа подготовки Middle/Senior Backend инженеров</p>
          </div>
        </div>

        {/* Progress & Actions */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3 bg-slate-100 px-4 py-2 rounded-xl border border-slate-200">
            <Award className="w-5 h-5 text-indigo-500" />
            <div>
              <div className="text-xs text-slate-500">Прогресс обучения</div>
              <div className="text-sm font-semibold flex items-center gap-2">
                <span>{completedTasks} / {totalTasks} тем</span>
                <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-medium">
                  {percent}%
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-800 px-4 py-2 rounded-xl border border-slate-200 transition active:scale-95 disabled:opacity-50 cursor-pointer"
            title="Обновить прогресс и запустить ментор"
          >
            <RefreshCw className={`w-4 h-4 text-indigo-600 ${loading ? "animate-spin" : ""}`} />
            <span className="text-sm font-medium">Синхронизировать</span>
          </button>
        </div>

      </div>
    </header>
  );
}