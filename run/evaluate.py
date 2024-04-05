import run.run_java as rj
import json
import run.error as error
from functools import lru_cache
import os
import func_timeout
import run.checker as checker

config=json.load(open('config.json','r',encoding='utf-8'))

def evaluate(origin, name):
    if (os.name == 'nt'):
        program_path = '.\\tools\\datainput_student_win64.exe'
    else:
        program_path = './tools/datainput_student_linux_x86_64'
    output = ""
    run_time = 0
    try:
        output, run_time = rj.execute_java_with_program(name, program_path)
        output = output.replace('\r', '')
    except func_timeout.exceptions.FunctionTimedOut as e:
        error.error_output(name, "Time Limit Exceeded", origin, "", e)
        return False, 0
    return checker.check(origin, output, name), run_time