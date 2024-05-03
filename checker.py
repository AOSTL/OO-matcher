import error as error
import json
config = json.load(open('config.json'))

def check(intput_str, output_str, name, ans):
    intput_str = _trim(intput_str)
    if (ans == output_str):
        return True
    error_path = config["error_folder_name"]
    if output_str == "" or output_str == None:
        error.error_output(name, "Runtime Error", intput_str, "", "No More Infomation", ans, error_path)
    elif "Error" in output_str:
        error.error_output(name, "Runtime Error", intput_str, output_str, "No More Infomation", ans, error_path)
    elif "Unreachable" in output_str:
        error.error_output(name, "Runtime Error", intput_str, output_str, "FOUND UNREACHABLE", ans, error_path)
    else:
        error.error_output(name, "Wrong Answer", intput_str, output_str, "No More Infomation", ans, error_path)
    return False


def _trim(s):
    if s[:1] != ' ' and s[-1:] != ' ' and s[:1] != '\n' and s[-1:] != '\n':
        return s
    elif s[:1] == ' ' or s[:1] == '\n':
        return _trim(s[1:])
    else:
        return _trim(s[:-1])