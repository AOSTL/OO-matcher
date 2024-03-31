import run_java
import re
import json
import error
from functools import lru_cache
import os
import func_timeout
import checker

config=json.load(open('config.json','r',encoding='utf-8'))

def evaluate(origin, name):
    if (os.name == 'nt'):
        program_path = '.\\tools\\datainput_student_win64.exe'
    else:
        program_path = './tools/datainput_student_linux_x86_64'
    output = ""
    run_time = 0
    try:
        output, run_time = run_java.execute_java_with_program(name, program_path)
    except func_timeout.exceptions.FunctionTimedOut as e:
        error.error_output(name, "Time Limit Exceeded", origin, "", e)
        return False, 0
    return checker.check(origin, output, name), run_time