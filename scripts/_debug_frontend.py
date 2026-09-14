import os
import subprocess
import sys
import time
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
log_path = ROOT / 'logs' / 'frontend_debug.log'
with open(log_path, 'w', encoding='utf-8') as log_f:
    # Вариант 1: cmd /c npm
    cmd1 = ['cmd.exe', '/c', 'npm', 'run', 'dev', '--', '--port', '5173', '--strictPort']
    # Вариант 2: напрямую node на vite
    vite_js = ROOT / 'frontend' / 'node_modules' / 'vite' / 'bin' / 'vite.js'
    cmd2 = [sys.executable, str(vite_js), '--port', '5173', '--strictPort']

    flags = (
        subprocess.CREATE_NEW_PROCESS_GROUP
        | subprocess.DETACHED_PROCESS
        | subprocess.CREATE_NO_WINDOW
    )
    log_f.write(f'cwd exists: {(ROOT / "frontend").exists()}\n')
    log_f.write(f'vite.js exists: {vite_js.exists()}\n')
    log_f.flush()

    for name, cmd in [('via-cmd-npm', cmd1), ('via-py-vite', cmd2)]:
        log_f.write(f'--- try {name}: {cmd}\n')
        log_f.flush()
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=ROOT / 'frontend',
                creationflags=flags,
            )
            log_f.write(f'spawned pid={proc.pid}\n')
            log_f.flush()
            time.sleep(6)
            rc = proc.poll()
            log_f.write(f'after 6s poll={rc}\n')
            if rc == 0:
                log_f.write('exited cleanly -> stopping\n')
                break
            if rc is None:
                log_f.write('still running -> stopping\n')
                subprocess.run(['taskkill', '/pid', str(proc.pid), '/f'], capture_output=True)
                break
            log_f.write('trying next variant\n')
        except Exception as exc:
            log_f.write(f'ERROR: {exc!r}\n')
            log_f.flush()
print('done')