import os
import subprocess
import sys
from pathlib import Path

# Фоновый запуск dev-серверов (FastAPI + Vite) с PID-файлами и логами.
# Использование:
#   py scripts/start_dev.py            # запустить оба сервера
#   py scripts/start_dev.py backend    # только API (порт 8000)
#   py scripts/start_dev.py frontend   # только Vite (порт 5173)
#   py scripts/start_dev.py stop       # остановить по PID-файлам

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

PID_FILES = {
    'backend': ROOT / '.dev_backend_pid',
    'frontend': ROOT / '.dev_frontend_pid',
}
LOG_FILES = {
    'backend': LOGS_DIR / 'backend.log',
    'frontend': LOGS_DIR / 'frontend.log',
}
BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'server:app', '--host', '127.0.0.1', '--port', '8000']

# Запускаем Vite напрямую через node.exe: npm.cmd не работает в DETACHED_PROCESS.
NODE_EXE = r'C:\Program Files\nodejs\node.exe'
VITE_JS = ROOT / 'frontend' / 'node_modules' / 'vite' / 'bin' / 'vite.js'
FRONTEND_CMD = [
    NODE_EXE,
    str(VITE_JS),
    '--host', '127.0.0.1',   # IPv4: браузер открывает localhost через 127.0.0.1
    '--port', '5173',
    '--strictPort',
]


def _spawn_kwargs() -> dict:
    # Изоляция от родительской консоли: run-сессия не смогла бы убить процесс.
    if os.name != 'nt':
        return {}
    return {
        'creationflags': (
            subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NO_WINDOW
        ),
    }


def restart(target: str) -> None:
    # Остановить прежний процесс (если жив/остался PID-файл) и запустить заново.
    pid_file = PID_FILES[target]
    if pid_file.exists():
        pid = pid_file.read_text().strip()
        if pid:
            subprocess.run(['taskkill', '/pid', pid, '/f'], capture_output=True)
            print(target, 'stopped stale pid', pid)
        pid_file.unlink(missing_ok=True)
    start(target)


def start(target: str) -> None:
    log_f = LOG_FILES[target].open('w', encoding='utf-8')
    cmd = BACKEND_CMD if target == 'backend' else FRONTEND_CMD
    kwargs = {'cwd': ROOT if target == 'backend' else ROOT / 'frontend'}
    kwargs.update(_spawn_kwargs())
    proc = subprocess.Popen(cmd, stdout=log_f, stderr=subprocess.STDOUT, **kwargs)
    PID_FILES[target].write_text(str(proc.pid), encoding='utf-8')
    print(target, 'started pid=' + str(proc.pid), 'log=' + str(LOG_FILES[target]))


def stop_all() -> None:
    for target, pid_file in PID_FILES.items():
        if pid_file.exists():
            pid = pid_file.read_text().strip()
            if pid:
                subprocess.run(['taskkill', '/pid', pid, '/f'], capture_output=True)
                print(target, 'pid', pid, 'terminated')
            pid_file.unlink(missing_ok=True)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == 'stop':
        stop_all()
        return
    targets = {'all': ['backend', 'frontend']}.get(args[0], [args[0]])
    for t in targets:
        if t not in PID_FILES:
            print('unknown target:', t, file=sys.stderr)
            sys.exit(2)
        restart(t)


if __name__ == '__main__':
    main()