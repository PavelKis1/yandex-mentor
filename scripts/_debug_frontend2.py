import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
log_path = ROOT / 'logs' / 'frontend_debug.log'

with open(log_path, 'w', encoding='utf-8') as log_f:
    # Try various flag combos
    cwd = ROOT / 'frontend'
    npm_cmd = r'C:\Program Files\nodejs\npm.cmd'

    flags_sets = [
        ('detached+no_window',
         subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
         [npm_cmd, 'run', 'dev', '--', '--port', '5173', '--strictPort']),
        ('detached_only',
         subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
         [npm_cmd, 'run', 'dev', '--', '--port', '5173', '--strictPort']),
        ('no_window_only',
         subprocess.CREATE_NO_WINDOW,
         [npm_cmd, 'run', 'dev', '--', '--port', '5173', '--strictPort']),
    ]

    for name, flags, cmd in flags_sets:
        log_f.write(f'--- {name}: {cmd}\n')
        log_f.flush()
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=str(cwd),
                creationflags=flags,
            )
            log_f.write(f'spawned pid={proc.pid}\n')
            log_f.flush()
            time.sleep(8)
            rc = proc.poll()
            log_f.write(f'after 8s poll={rc}\n')
            log_f.flush()
            if rc is None:
                log_f.write('STILL RUNNING! This is the one.\n')
                subprocess.run(['taskkill', '/pid', str(proc.pid), '/f'], capture_output=True)
                # save pid for future use
                (ROOT / '.dev_frontend_pid').write_text(str(proc.pid), encoding='utf-8')
                break
            else:
                log_f.write(f'exited with code {rc}\n')
                subprocess.run(['taskkill', '/pid', str(proc.pid), '/f'], capture_output=True)
        except Exception as exc:
            log_f.write(f'ERROR: {exc!r}\n')
            log_f.flush()
print('debug done')