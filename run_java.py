import time
import subprocess
from subprocess import STDOUT, PIPE

def execute_java(stdin, name):
    cmd = ['java', '-jar', name]
    start_time = time.time()
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    end_time = time.time()
    stdout, stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip(), end_time - start_time