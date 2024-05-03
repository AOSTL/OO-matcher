import subprocess
from subprocess import STDOUT, PIPE
import time
import os

def time_exceeded(signo, frame):
    print("time's up")
    raise SystemExit(1)


def set_max_runtime(seconds):
    import resource, signal
    soft,hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    signal.signal(signal.SIGXCPU, time_exceeded)


def execute_java(stdin, name):
    if os.name != 'nt':
        set_max_runtime(12)
    if name[-4:] != '.jar':
        name += '.jar'
    cmd = ['java', '-jar', name]
    start_time = time.time()
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout = ""
    if os.name == 'nt':
        stdout, stderr = proc.communicate(stdin.encode(), timeout=11)
    else:
        stdout, stderr = proc.communicate(stdin.encode(), timeout=120)
    end_time = time.time()
    output = stdout.decode().strip()
    first_line, *_ = output.partition('\n')
    if first_line.__contains__('warning'):
        output = '\n'.join(output.split('\n')[1:])
    return output, end_time - start_time
