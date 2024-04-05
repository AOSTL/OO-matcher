from run.object import PASSANGER
from run.object import arrive, open, close, passanger_in, passanger_out, passanger_receive, reset_accepted, reset_begin, reset_end
import re

def input_ana(origin):
    lines = origin.split('\n')
    passangers = {}
    for line in lines:
        if match := re.match(r'^\[.*\](\d+)-FROM-(\d+)-TO-(\d+)', line):
            passangers[int(match.group(1))] = PASSANGER(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return passangers


def output_ana(output):
    lines = output.split('\n')
    actions = []
    for line in lines:
        if match := re.match(r'^\[\s*([\d\.]*)\]ARRIVE-(\d+)-(\d+)$', line):
            actions.append(arrive(float(match.group(1)), 'ARRIVE', int(match.group(2)), int(match.group(3))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]OPEN-(\d+)-(\d+)$', line):
            actions.append(open(float(match.group(1)), 'OPEN', int(match.group(2)), int(match.group(3))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]CLOSE-(\d+)-(\d+)$', line):
            actions.append(close(float(match.group(1)), 'CLOSE', int(match.group(2)), int(match.group(3))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]IN-(\d+)-(\d+)-(\d+)$', line):
            actions.append(passanger_in(float(match.group(1)), 'IN', int(match.group(2)), int(match.group(3)), int(match.group(4))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]OUT-(\d+)-(\d+)-(\d+)$', line):
            actions.append(passanger_out(float(match.group(1)), 'OUT', int(match.group(2)), int(match.group(3)), int(match.group(4))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]RECEIVE-(\d+)-(\d+)$', line):
            actions.append(passanger_receive(float(match.group(1)), 'RECEIVE', int(match.group(2)), int(match.group(3))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]RESET_ACCEPT-(\d+)-(\d+)-([\d\.]*)$', line):
            actions.append(reset_accepted(float(match.group(1)), 'RESET_ACCEPT', int(match.group(2)), int(match.group(3)), float(match.group(4))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]RESET_BEGIN-(\d+)$', line):
            actions.append(reset_begin(float(match.group(1)), 'RESET_BEGIN', int(match.group(2))))
        elif match := re.match(r'^\[\s*([\d\.]*)\]RESET_END-(\d+)$', line):
            actions.append(reset_end(float(match.group(1)), 'RESET_END', int(match.group(2))))
        else:
            return False, line
    return True, actions