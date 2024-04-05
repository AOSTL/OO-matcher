import run.error as error
import run.judge as judge
import run.analyse as analyse

def check(origin: str, output: str, name: str):
    origin = _trim(origin)
    output = _trim(output)
    passangers = analyse.input_ana(origin)
    format_avalable, actions = analyse.output_ana(output)
    if format_avalable == False:
        error.error_output(name, 'Format Error', origin, output, 'First Error Line: ' + actions)
        return False
    res = judge.judge(passangers, actions)
    if (res[0] == False):
        error.error_output(name, res[1], origin, output, res[2])
    return res[0]

def _trim(s):
    if s[:1] != ' ' and s[-1:] != ' ' and s[:1] != '\n' and s[-1:] != '\n':
        return s
    elif s[:1] == ' ' or s[:1] == '\n':
        return _trim(s[1:])
    else:
        return _trim(s[:-1])