import subprocess
import time
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
log_path = ROOT / 'logs' / 'frontend_debug.log'

with open(log_path, 'w', encoding='utf-8') as log_f:
    cwd = ROOT / 'frontend'
    node_exe = r'C:\Program Files\nodejs\node.exe'
    vite_js = ROOT / 'frontend' / 'node_modules' / 'vite' / 'bin' / 'vite.js'
    cmd = [node_exe, str(vite_js), '--port', '5173', '--strictPort']
    flags = (
        subprocess.CREATE_NEW_PROCESS_GROUP
        | subprocess.DETACHED_PROCESS
        | subprocess.CREATE_NO_WINDOW
    )
    log_f.write(f'node={node_exe}\nvite={vite_js}\ncmd={cmd}\n')
    log_f.flush()
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            cwd=str(cwd),
            creationflags=flags,
        )
        (ROOT / '.dev_frontend_pid').write_text(str(proc.pid), encoding='utf-8')
        log_f.write(f'spawned pid={proc.pid}\n')
        log_f.flush()
        time.sleep(10)
        rc = proc.poll()
        log_f.write(f'after 10s poll={rc}\n')
        log_f.flush()
        if rc is None:
            log_f.write('STILL RUNNING\n')
        else:
            log_f.write(f'EXITED {rc}\n')
            (ROOT / '.dev_frontend_pid').unlink(missing_ok=True)
    except Exception as exc:
        log_f.write(f'ERROR: {exc!r}\n')
        log_f.flush()
print('debug done')