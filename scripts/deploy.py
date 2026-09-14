"""
Deploy roadmap to public URL using localhost.run tunnel.
Run: py scripts/deploy.py
"""

import subprocess
import time
import sys
import re
import os


def main():
    print("[1/3] Starting local server on port 8765...")

    # Start server in background
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(2)
    print("[2/3] Server started. Creating SSH tunnel...")

    url = None
    tunnel = None
    try:
        # Start localhost.run tunnel (ssh -R) with custom key
        ssh_key = os.path.expanduser("~/.ssh/id_lr")
        tunnel = subprocess.Popen(
            ["ssh", "-i", ssh_key,
             "-o", "StrictHostKeyChecking=no",
             "-o", "ServerAliveInterval=60",
             "-R", "80:localhost:8765", "localhost.run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        print("[3/3] Waiting for public URL...")
        for line in tunnel.stdout:
            print(line.rstrip())
            match = re.search(r"https?://\S+\.lhr\.life", line)
            if match:
                url = match.group(0)
                break

        if url:
            print(f"\n{'='*60}")
            print(f"  PUBLIC URL: {url}")
            print(f"{'='*60}")
            print(f"\n  Open on any device (phone, tablet):")
            print(f"  -> {url}/roadmap.html")
            print(f"\n  To add as iPhone widget:")
            print(f"  1. Open {url}/roadmap.html in Safari")
            print(f"  2. Tap Share -> Add to Home Screen")
            print(f"\n  Press Ctrl+C to stop")
            print(f"{'='*60}\n")
            tunnel.wait()
        else:
            print("[ERROR] Could not get public URL. Is SSH installed?")
            tunnel.terminate()

    except FileNotFoundError:
        print("[ERROR] ssh not found. Install OpenSSH or use ngrok with authtoken.")
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")
    except Exception as e:
        print(f"[ERROR] Tunnel failed: {e}")
    finally:
        server.terminate()
        if tunnel is not None:
            tunnel.terminate()


if __name__ == "__main__":
    main()