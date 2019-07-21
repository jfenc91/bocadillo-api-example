# modeled from aws sagemaker templates

from __future__ import print_function
import multiprocessing
import os
import signal
import subprocess
import sys

adj_cpu_count = int(multiprocessing.cpu_count() * 1.8)
workers = int(os.environ.get("SERVER_WORKERS", adj_cpu_count))


def sigterm_handler(pids):
    for pid in pids:
        try:
            os.kill(pid, signal.SIGQUIT)
        except OSError:
            pass

    sys.exit(0)


def start_server():
    print("Starting server with {} workers.".format(workers))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(["ln", "-sf", "/dev/stdout", "/var/log/nginx/access.log"])
    subprocess.check_call(["ln", "-sf", "/dev/stderr", "/var/log/nginx/error.log"])

    nginx = subprocess.Popen(["nginx", "-c", "/usr/src/app/nginx.conf"])
    gunicorn = subprocess.Popen(
        [
            "uvicorn",
            "--uds",
            "/tmp/gunicorn.sock",
            "--workers",
            str(workers),
            "asgi:app",
        ]
    )

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # If either subprocess exits, so do we.
    pids = set([nginx.pid, gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(pids)
    print("Inference server exiting")


if __name__ == "__main__":
    start_server()
