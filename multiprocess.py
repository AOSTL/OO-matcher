import threading
import time
import os
from colorama import Fore, Back, Style
import func_timeout
import generate
import run_java
import error
import checker
import json
import subprocess
config = json.load(open('config.json'))

wrong = 0
tle = 0

def evaluate(origin, name, ans):
    output = ""
    run_time = 0
    try:
        output, run_time = run_java.execute_java(origin, name)
        output = output.replace('\r', '')
    except subprocess.TimeoutExpired as e:
        error.error_output(name, "Time Limit Exceeded", origin, "", e, ans, error_path = config["error_folder_name"])
        return False, 0
    return checker.check(origin, output, name, ans), run_time


def fun(input_str, name, jar_file, interact, ans):
    global wrong
    global tle
    try:
        res, run_time = evaluate(input_str, name, ans)
        if (interact):
            if (res == False):
                print(str(name) + ": " + Fore.RED + "Wrong or TLE" + Fore.WHITE)
                wrong += 1
            else:
                print(str(name) + ": " + Fore.GREEN + "Accepted" + Fore.WHITE + " with " + str(run_time) + "s")
        elif (res == False):
            wrong += 1
    except Exception as e:
        wrong += 1
        if (interact):
            print(str(os.path.basename(jar_file)) + ": " + Fore.RED + "Error" + Fore.WHITE)
        error.error_output(name, "Unkown Error", input_str, "", e, ans, error_path = config["error_folder_name"])


def run(jar_files, interact):
    global tle, wrong
    test_case = 0
    while True:
        test_case += 1
        input_str = generate.genCommands()
        if (interact):
            print("---->   epoch " + str(test_case) + "   ---   wrong: " + str(wrong) + "   ---   tle: " + str(tle) + "   <----")
            print(str(input_str.count('\n')) + " lines")

        ans = ""
        try:
            ans = run_java.execute_java(input_str, 'zyt.jar')[0].replace('\r', '')
        except subprocess.TimeoutExpired as e:
            tle = tle + 1
            continue
        except Exception as e:
            error.error_output("STD", "Fatal Error", input_str, "", e, ans, error_path = config["error_folder_name"])
            continue

        with open("ans.txt", "w") as f:
            f.write(ans)

        threads = []
        for jar_file in jar_files:
            name = ""
            if (os.name == 'nt'):
                name = os.path.splitext(jar_file)[0].split("\\")[1]
            else:
                name = os.path.splitext(jar_file)[0].split("/")[1]

            thread = threading.Thread(target=fun, args = (input_str, name, jar_file, interact, ans))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if (interact):
            time.sleep(0.75)
        else:
            with open ("matcher.log", "w") as f:
                f.write("epoch: " + str(test_case) + " Wrong: " + str(wrong) + " TLE: " + str(tle) + "\n")

