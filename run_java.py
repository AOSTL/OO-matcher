import subprocess
from subprocess import STDOUT, PIPE
from func_timeout import func_set_timeout
import time

@func_set_timeout(120)
def execute_java(stdin, name):
    cmd = ['java', '-jar', name]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

@func_set_timeout(90)
def execute_java_with_program(name, input_program):
    input_proc_cmd = [input_program]
    input_proc = subprocess.Popen(input_proc_cmd, stdout=subprocess.PIPE)
    grep_command = ['java', '-jar', name + '.jar']
    start_time = time.time()
    grep_process = subprocess.Popen(grep_command, stdin=input_proc.stdout, stdout=subprocess.PIPE)
    output, _ = grep_process.communicate()
    end_time = time.time()
    return output.decode().strip(), end_time - start_time

def execute_py(stdin, name):
    cmd = ['py', name]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()
