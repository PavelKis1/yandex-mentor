import { Terminal } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 text-slate-500 py-6 text-xs">
      <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-500" />
          <span>Yandex Backend Mentor Platform • All 69 Topics Ready</span>
        </div>
        <div>Senior Backend Architect / Staff Engineer Standard</div>
      </div>
    </footer>
  );
}