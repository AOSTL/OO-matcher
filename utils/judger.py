from utils.params import *
from utils.elevator import Elevator
from utils.floor import Floor
from utils.person import Person
import copy

def prework(output):
    '''
    输入为若干行字符串
    每行字符串格式：
    电梯到达某一位置：[时间戳]ARRIVE-所在层-电梯ID
    电梯开始开门：[时间戳]OPEN-所在层-电梯ID
    电梯完成关门：[时间戳]CLOSE-所在层-电梯ID
    乘客进入电梯：[时间戳]IN-乘客ID-所在层-电梯ID
    乘客离开电梯：[时间戳]OUT-乘客ID-所在层-电梯ID
    电梯接收到重置请求：[时间戳]RESET_ACCEPT-电梯ID-满载人数-移动一层的时间(单位s)
    电梯开始重置：[时间戳]RESET_BEGIN-电梯ID
    电梯重置完成：[时间戳]RESET_END-电梯ID
    电梯接收分配：[时间戳]RECEIVE-乘客ID-电梯ID
    返回格式：
    action = [时间戳, 动作, 位置, 电梯ID] | [时间戳, 动作, 位置, 电梯ID, 乘客ID]
                | [时间戳, 动作, 电梯ID] | [时间戳, 动作, 电梯ID, 乘客ID]
                | [时间戳, 动作, 电梯ID, 满载人数, 移动一层时间]
    '''
    # W: [ARRIVE, OPEN, CLOSE, SUM]
    W = [0] * 3
    actions = []
    for line in output:
        line = line.strip().replace(' ', '')
        # print(line[1:line.find(']')])
        time = float(line[1:line.find(']')])
        action = line[line.find(']') + 1:].split('-')
        if action[0] == 'ARRIVE':
            actions.append([time, ACTION_ARRIVE, int(action[1]), int(action[2])])
            W[0] += 1
        elif action[0] == 'OPEN':
            actions.append([time, ACTION_OPEN, int(action[1]), int(action[2])])
            W[1] += 1
        elif action[0] == 'CLOSE':
            actions.append([time, ACTION_CLOSE, int(action[1]), int(action[2])])
            W[2] += 1
        elif action[0] == 'IN':
            actions.append([time, ACTION_IN, int(action[2]), int(action[3]), int(action[1])])
        elif action[0] == 'OUT':
            actions.append([time, ACTION_OUT, int(action[2]), int(action[3]), int(action[1])])
        elif action[0] == 'RESET_ACCEPT':
            actions.append([time, ACTION_RESET_ACCEPT, int(action[1]), int(action[2]), float(action[3])])
        elif action[0] == 'RESET_BEGIN':
            actions.append([time, ACTION_RESET_BEGIN, int(action[1])])
        elif action[0] == 'RESET_END':
            actions.append([time, ACTION_RESET_END, int(action[1])])
        elif action[0] == 'RECEIVE':
            actions.append([time, ACTION_RECEIVE, int(action[2]), int(action[1])])
        else:
            raise Exception(f'prework: unknown action {action}')
    W.append((W[0] * W_ARRIVE + W[1] * W_OPEN + W[2] * W_CLOSE) / 10)
    return actions, W

class Judger:
    def __init__(self) -> None:
        self.personList = []
        
    def __init__(self, input) -> None:
        '''
        1.输入格式
        每个乘客由指定的电梯从起点层接送到终点层。
        格式为：
        [时间戳]乘客ID-FROM-起点层-TO-终点层
        [时间戳]RESET-Elevator-电梯ID-满载人数-移动一层的时间(单位s)
        '''
        input = input.strip().split('\n')
        self.personList = []
        for line in input:
            if 'RESET' in line:
                continue
            line = line.strip().replace(' ', '')
            time = float(line[1:line.find(']')])
            person = line[line.find(']') + 1:].split('-')
            self.personList.append(Person([time, int(person[0]), int(person[2]), int(person[4]), int(person[2])]))
    
    def addPerson(self, person: Person):
        self.personList.append(person)
    
    def judge(self, output):
        '''
        output: str List 输出
        '''
        elevators = [Elevator(i) for i in range(1, ELE_NUMBER + 1)]
        floors = [Floor(i) for i in range(MIN_FLOOR, MAX_FLOOR + 1)]
        for person in self.personList:
            floors[person.now - 1].addPerson(copy.deepcopy(person))
        
        actions, W = prework(output)
        '''
        action = [时间戳, 动作, 位置, 电梯ID] | [时间戳, 动作, 位置, 电梯ID, 乘客ID]
            | [时间戳, 动作, 电梯ID] | [时间戳, 动作, 电梯ID, 乘客ID]
            | [时间戳, 动作, 电梯ID, 满载人数, 移动一层时间]
        '''
        for i in range(len(actions)):
            action = actions[i]
            try:
                if action[1] == ACTION_ARRIVE: # [时间戳, 动作, 位置, 电梯ID]
                    elevators[action[3] - 1].arrive(action[0], action[2])
                elif action[1] == ACTION_OPEN: # [时间戳, 动作, 位置, 电梯ID]
                    elevators[action[3] - 1].open(action[0], action[2])
                elif action[1] == ACTION_CLOSE: # [时间戳, 动作, 位置, 电梯ID]
                    elevators[action[3] - 1].close(action[0], action[2])
                elif action[1] == ACTION_IN: # [时间戳, 动作, 位置, 电梯ID, 乘客ID]
                    elevators[action[3] - 1].addPerson(floors[action[2] - 1].popPerson(action[4]), action[0])
                elif action[1] == ACTION_OUT: # [时间戳, 动作, 位置, 电梯ID, 乘客ID]
                    floors[action[2] - 1].addPerson(elevators[action[3] - 1].popPerson(action[4]), action[0])
                elif action[1] == ACTION_RESET_ACCEPT: # [时间戳, 动作, 电梯ID, 满载人数, 移动一层时间]
                    elevators[action[2] - 1].resetAccept(action[0], action[3], action[4])
                elif action[1] == ACTION_RESET_BEGIN: # [时间戳, 动作, 电梯ID]
                    elevators[action[2] - 1].resetBegin(action[0])
                    for floor in floors:
                        floor.resetBegin(action[2])
                elif action[1] == ACTION_RESET_END: # [时间戳, 动作, 电梯ID]
                    elevators[action[2] - 1].resetEnd(action[0])
                elif action[1] == ACTION_RECEIVE: # [时间戳, 动作, 电梯ID, 乘客ID]
                    if elevators[action[2] - 1].resetBeginTime != None:
                        raise Exception(f'judge: elevator {action[2]} is in reset, can not receive person {action[3]}')
                    fl = 0
                    for floor in floors:
                        if floor.receive(action[3], action[2]):
                            fl = 1
                            break
                    if fl == 0:
                        raise Exception(f'judge: no person {action[2]} received')
                    elevators[action[2] - 1].receiveCnt += 1
                else:
                    raise Exception(f'judge: unknown action {action}')
            except Exception as e:
                raise Exception(output[i] + f'\n{e}')
        
        MT = -10**9
        for floor in floors:
            MT = max(MT, floor.check())
        for elevator in elevators:
            elevator.check()
        
        return MT, W
        
        
        