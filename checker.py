import re
import json
import error

config = json.load(open('config.json', 'r'))

def check(origin: str, output: str, name: str):
    origin = trim(origin)
    output = trim(output)
    waiters = analyze_input(origin)
    if type(waiters) == str:
        error.error_output(name, 'Format Error', origin, output, waiters)
        return False
    actions = analyze_output(output)
    if type(actions) == str:
        error.error_output(name, 'Format Error', origin, output, actions)
        return actions
    res = imitate(waiters, actions)
    if (res[0] == False):
        error.error_output(name, res[1], origin, output, 'On line ' + str(res[2]) + ' .')
    return res[0]

def analyze_input(origin: str) -> dict[int, list[int, int, float]] | str:
    lines = origin.split('\n')
    waiters = {}
    for i in range(len(lines)):
        line = lines[i]
        if 'RESET' in line:
            continue
        matcher = re.match(r'\[\s*(\d+\.\d+)\](\d+)-FROM-(\d+)-TO-(\d+)', line)
        waiters[int(matcher.group(2))] = [float(matcher.group(1)), int(matcher.group(3)), int(matcher.group(4))]
    return waiters


# 将输出拆分为每个电梯的行为
def analyze_output(output: str) -> list | str:
    lines = output.split('\n')
    actions = []
    for i in range(len(lines)):
        line = lines[i]
        matcher = re.match(r'\[\s*(\d+\.\d+)\]([A-Z_]+).*', line)
        try:
            if matcher.group(2) in ['ARRIVE', 'OPEN', 'CLOSE', 'RECEIVE']:
                matcher = re.match(r'\[\s*(\d+\.\d+)\]([A-Z_]+)-(\d+)-(\d+)', line)
                actions.append(
                    [float(matcher.group(1)), matcher.group(2), int(matcher.group(3)), int(matcher.group(4))])
            elif matcher.group(2) in ['IN', 'OUT']:
                matcher = re.match(r'\[\s*(\d+\.\d+)\]([A-Z_]+)-(\d+)-(\d+)-(\d+)', line)
                actions.append([float(matcher.group(1)), matcher.group(2), int(matcher.group(3)), int(matcher.group(4)),
                                int(matcher.group(5))])
            elif matcher.group(2) == 'RESET_ACCEPT':
                matcher = re.match(r'\[\s*(\d+\.\d+)\]([A-Z_]+)-(\d+)-(\d+)-(\d+\.\d+)', line)
                actions.append([float(matcher.group(1)), matcher.group(2), int(matcher.group(3)), int(matcher.group(4)),
                                float(matcher.group(5))])
            elif matcher.group(2) in ['RESET_BEGIN', 'RESET_END']:
                matcher = re.match(r'\[\s*(\d+\.\d+)\]([A-Z_]+)-(\d+)', line)
                actions.append([float(matcher.group(1)), matcher.group(2), int(matcher.group(3))])
            else:
                return 'Error on line ' + str(i + 1) + '.'
        except:
            return 'Error on line ' + str(i + 1) + '.'
    return actions

def imitate(waiters, actions) -> str:
    elevators = [elevator() for i in range(7)]
    received_waiters = {}
    tolerance = 0.02

    for i in range(0, len(actions)):
        action = actions[i]
        match action[1]:
            case 'RESET_ACCEPT':
                if elevators[action[2]].reset != []:
                    return False, 'RESET_ACCEPT before RESET_END', i + 1
                elevators[action[2]].reset.append(action)
                elevators[action[2]].reset_floor = 0
            case 'RESET_BEGIN':
                if elevators[action[2]].reset.__len__() != 1 or elevators[action[2]].reset[0][1] != 'RESET_ACCEPT':
                    return False, 'Unauthorized Reset', i + 1
                elif elevators[action[2]].passengers != {}:
                    return False, 'RESET_BEGIN with passengers', i + 1
                elif elevators[action[2]].last_closetime < elevators[action[2]].last_opentime:
                    return False, 'RESET_BEGIN with door open', i + 1
                elif elevators[action[2]].reset_floor > 2:  # 没有容错
                    return False, 'RESET_BEGIN to RESET_END over 2 floors', i + 1
                for p in elevators[action[2]].receiver:  # 取消分配
                    waiters[p] = elevators[action[2]].receiver[p]
                    received_waiters.pop(p)
                elevators[action[2]].receiver.clear()
                elevators[action[2]].reset.append(action)
            case 'RESET_END':
                if elevators[action[2]].reset.__len__()!=2 or not ('RESET_ACCEPT' in elevators[action[2]].reset[0] and 'RESET_BEGIN' in elevators[action[2]].reset[1]):
                    return False, 'RESET_END without RESET_BEGIN', i + 1
                elif action[0]-elevators[action[2]].reset[0][0]>5+tolerance:  #没有容错
                    return False, 'RESET_ACCEPT to RESET_END over 5s', i + 1
                elif action[0]-elevators[action[2]].reset[1][0]<1.2-tolerance:    #有容错
                    return False, 'RESET_BEGIN to RESET_END under 1.2s', i + 1
                elevators[action[2]].capacity=elevators[action[2]].reset[0][3]
                elevators[action[2]].speed=elevators[action[2]].reset[0][4]
                elevators[action[2]].reset=[]
                elevators[action[2]].reset_floor=0
            case 'RECEIVE':
                # 同一乘客被分配到多个电梯、多次输出receive
                if action[2] in received_waiters.keys():
                    return False, 'Repeated Receive', i + 1
                elif action[2] not in waiters.keys():
                    return False, 'Receive without Passanger', i + 1
                elif elevators[action[3]].reset.__len__() == 2:
                    return False, 'Receive during Reset', i + 1
                received_waiters[action[2]] = waiters[action[2]]
                elevators[action[3]].receiver[action[2]] = waiters[action[2]]
                waiters.pop(action[2])
            case 'ARRIVE':
                if action[2]>11 or action[2]<1:
                    return False, 'Arrive out of range', i + 1
                elif action[0]-elevators[action[3]].last_arrivetime<elevators[action[3]].speed-tolerance:
                    return False, 'Move too fast', i + 1
                elif elevators[action[3]].last_opentime>elevators[action[3]].last_closetime:
                    return False, 'Move with door open', i + 1
                elif elevators[action[3]].passengers==[] and elevators[action[3]].receiver=={}:
                    return False, 'Move without Rceive', i + 1
                elif elevators[action[3]].reset.__len__()==2:
                    return False, 'Move during Reset', i + 1
                elif abs(elevators[action[3]].floor-action[2])!=1:
                    return False, 'Move over 1 floor', i + 1
                elevators[action[3]].floor=action[2]
                elevators[action[3]].last_arrivetime=action[0]
                elevators[action[3]].reset_floor+=1
            case 'OPEN':
                if elevators[action[3]].reset.__len__() == 2:
                    return False, 'Open during Reset', i + 1
                elif elevators[action[3]].floor != action[2]:
                    return False, 'Open Not on Arrived Floor', i + 1
                elif elevators[action[3]].last_opentime > elevators[action[3]].last_closetime:
                    return False, 'Open with door open', i + 1
                elevators[action[3]].last_opentime = action[0]
            case 'CLOSE':
                if elevators[action[3]].reset.__len__() == 2:
                    return False, 'Close during Reset', i + 1
                elif elevators[action[3]].floor != action[2]:
                    return False, 'Close Not on Arrived Floor', i + 1
                elif elevators[action[3]].last_opentime < elevators[action[3]].last_closetime:
                    return False, 'Close with door closed', i + 1
                elif action[0] - elevators[action[3]].last_opentime < elevators[action[3]].open_time + elevators[action[3]].close_time - tolerance:
                    return False, 'Close too fast', i + 1
                elevators[action[3]].last_closetime = action[0]
            case 'IN':
                if elevators[action[4]].reset.__len__() == 2:
                    return False, 'In during Reset', i + 1
                elif elevators[action[4]].floor != action[3]:
                    return False, 'In Not on Arrived Floor', i + 1
                elif elevators[action[4]].last_opentime < elevators[action[4]].last_closetime:
                    return False, 'In with door closed', i + 1
                elif elevators[action[4]].passengers.__len__() + 1 > elevators[action[4]].capacity:
                    return False, 'Overloaded', i + 1
                elif action[2] not in elevators[action[4]].receiver.keys():
                    return False, 'In without Receive', i + 1
                elif received_waiters[action[2]][1] != action[3]:
                    return False, 'In on wrong floor', i + 1
                elevators[action[4]].passengers[action[2]] = received_waiters[action[2]]
            case 'OUT':
                if elevators[action[4]].reset.__len__() == 2:
                    return False, 'Out during Reset', i + 1
                elif elevators[action[4]].floor != action[3]:
                    return False, 'Out Not on Arrived Floor', i + 1
                elif elevators[action[4]].last_opentime < elevators[action[4]].last_closetime:
                    return False, 'Out with door closed', i + 1
                elif action[2] not in elevators[action[4]].passengers.keys():
                    return False, 'Out without In', i + 1
                if elevators[action[4]].passengers[action[2]][2] != action[3]:
                    waiters[action[2]] = elevators[action[4]].passengers[action[2]]
                    waiters[action[2]][1] = action[3]
                elevators[action[4]].receiver.pop(action[2])
                received_waiters.pop(action[2])
                elevators[action[4]].passengers.pop(action[2])
    for i in range(1, len(elevators)):
        if elevators[i].reset != []:
            return False, 'Thread End during Reset', -1
        if elevators[i].passengers != {}:
            return False, 'Thread End with passengers', -1
        if elevators[i].last_opentime > elevators[i].last_closetime:
            return False, 'Thread End with door open', -1
    if waiters != {}:
        return False, 'Passanger in Queue', -1
    return True, '', -1

class elevator:
    def __init__(self):
        self.capacity = 6
        self.speed = 0.4
        self.open_time= 0.2
        self.close_time= 0.2
        
        self.last_opentime = 0
        self.last_closetime = 1e-9
        self.last_arrivetime = 0
        self.floor = 1
        self.passengers = {}
        self.receiver = {}

        self.reset = []
        self.reset_floor = 0

def trim(s):
    if s[:1] != ' ' and s[-1:] != ' ' and s[:1] != '\n' and s[-1:] != '\n':
        return s
    elif s[:1] == ' ' or s[:1] == '\n':
        return trim(s[1:])
    else:
        return trim(s[:-1])