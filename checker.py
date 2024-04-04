import os
import error
import json

config = json.load(open("config.json", "r"))


class Req:
    def __init__(self, req):
        eles = self.parseReq(req)
        self.passenger_id = int(eles[0])
        self.ff = int(eles[2])
        self.tf = int(eles[4])
        self.cf = -1    # 最终到达的楼层
        self.r = False  # receive

    def parseReq(self, req):
        req = req.replace('\n', '')
        index = req.index(']')
        req = req[index + 1:]
        return req.split('-')

    def getUserId(self):
        return self.passenger_id

    def getFromFloor(self):
        return self.ff

    def getToFloor(self):
        return self.tf

    def getReceive(self):
        return self.r

    def setFromFloor(self, ff):
        self.ff = ff

    def setCurFloor(self, cf):
        self.cf = cf

    def setReceive(self, r):
        self.r = r


STATE_OPEN = 0
STATE_CLOSE = 1
STATE_RESET_BEGIN = 2
STATE_RESET_END = 3
MAX_FLOOR = 11
MIN_FLOOR = 1

reqDict = {}
speeds = []  # 6 elevators速度，上下两层楼的时间
capacities = []  # 6 elevators容量
preSpeeds = []
preCapacities = []
floors = []  # 6 elevators上一个楼层
states = []  # 0 open, 1 close, 2 reset
passengers = {}  # 6 elevators上的乘客
receives = []  # 6 elevators 是否收到Recevive请求
allPassengers = []  # 所有乘客 passenger_id -> elevator_id[0-5]
lastMoveTime = []  # 6 elevators上一次移动时间点
lastOpenTime = []  # 6 elevators上一次开门时间点
lastOpTime = []  # 6 elevators上一次操作时间点
lastResetTime = []  # 6 elevators上一次reset时间点，set期间不允许open，close，in，out，receive

flag = [0]


def check(input_str, output_str, name):
    initElevator()
    processInput(input_str)
    flag[0] = 1
    count = 1
    lines = output_str.split('\n')
    for line in lines:
        if line != "":
            res = process(line, count)
            count += 1
            if not res[0]:
                error.error_output(
                    name, res[1], input_str, output_str, "Line: " + str(res[2]))
                return False

    if len(reqDict) != 0:
        missing = ""
        for req in reqDict.values():
            missing += str(req.getUserId()) + "\n"
        error.error_output(name, "Not all requests are processed",
                           input_str, output_str, "Missing: " + missing)
        return False
    for i in range(6):
        if len(passengers[i]) != 0:
            error.error_output(name, "Someone is trapped in elevator", input_str, output_str,
                               "Elevator ID: " + str(i + 1))
        if states[i] != STATE_CLOSE:
            error.error_output(name, "Elevator door is not close",
                               input_str, output_str, "Elevator ID: " + str(i + 1))
            return False
    if flag[0] == 1:
        return True


def initElevator():
    reqDict.clear()
    speeds.clear()
    capacities.clear()
    floors.clear()
    states.clear()
    passengers.clear()
    receives.clear()
    allPassengers.clear()
    lastMoveTime.clear()
    lastOpenTime.clear()
    lastOpTime.clear()
    lastResetTime.clear()

    flag[0] = 0
    for i in range(6):
        floors.append(1)
        states.append(STATE_CLOSE)
        passengers.append([])
        lastMoveTime.append(-10.0)
        lastOpenTime.append(-10.0)
        lastOpTime.append(0.0)
        lastResetTime.append(0.0)
        speeds.append(0.4)
        capacities.append(6)


def processInput(input_str):
    tot = input_str.split('\n')
    for ele in tot:
        if (ele == ""):
            break
        req = Req(ele)
        reqDict[req.getUserId()] = req


def process(read, lineNum):
    read = read.replace('\n', '')
    index = read.index(']')
    opTime = float(read[1:index - 1])
    read = read[index + 1:]
    eles = read.split('-')

    if (opTime < lastOpTime[0]):
        return False, "INCORRECT OUTPUT ORDER!", lineNum

    lastOpTime[0] = opTime

    if eles[0] == 'ARRIVE':
        index = int(eles[2]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELECATOR ID!", lineNum
        if states[index] != STATE_CLOSE:
            return False, "MOVE WHEN DOOR IS NOT CLOSE!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "MOVE WHEN RESET BEGIN!", lineNum
        if receives[index] == False:
            return False, "NO RECEIVE BEFORE MOVE!", lineNum
        # 小抖动误差
        if opTime - lastMoveTime[index] < speeds[index] - float(config["fault_tolerance"]):
            return False, "MOVE TOO FAST!", lineNum
        lastMoveTime[index] = opTime
        if int(eles[1]) > MAX_FLOOR or int(eles[1]) < MIN_FLOOR:
            return False, "ELEVATOR ON A NON-EXISTENT FLOOR!", lineNum
        if floors[index] - int(eles[1]) != 1 and floors[index] - int(eles[1]) != -1:
            return False, "ELEVATOR MOVE TOO FAST!", lineNum
        floors[index] = int(eles[1])

    elif eles[0] == 'OPEN':
        index = int(eles[2]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_CLOSE:
            return False, "ELEVATOR ALREADY OPEN!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "OPEN WHEN RESET BEGIN!", lineNum
        states[index] = STATE_OPEN
        lastOpTime[index] = opTime
        if floors[index] != int(eles[1]):
            return False, "ELEVATOR UNMATCHED FLOOR!", lineNum

    elif eles[0] == 'CLOSE':
        index = int(eles[2]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_OPEN:
            return False, "ELEVATOR ALREADY CLOSE!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "CLOSE WHEN RESET BEGIN!", lineNum
        states[index] = STATE_CLOSE
        lastOpTime[index] = opTime
        if floors[index] != int(eles[1]):
            return False, "ELEVATOR UNMATCHED FLOOR!", lineNum
        if opTime - lastOpenTime[index] < 0.4 - 0.00001:
            return False, "CLOSE TOO FAST!", lineNum

    elif eles[0] == 'IN':
        index = int(eles[3]) - 1
        passenger_index = int(eles[1])
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_OPEN:
            return False, "PASSENGER IN WHEN DOOR IS NOT OPEN!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "IN WHEN RESET BEGIN!", lineNum
        allPassengers[passenger_index] = index
        req = reqDict.get(passenger_index)
        if req == None:
            return False, "PASSENGER NOT EXIST!", lineNum
        else:
            if req.getFromFloor() != int(eles[2]):
                return False, "IN MESSAGE NOT MATCH REQUEST!", lineNum
            if len(passengers[index]) > capacities[index]:
                return False, "ELEVATOR OVERLOAD!", lineNum
            if floors[index] != int(eles[2]):
                return False, "ELEVATOR UNMATCHED FLOOR!", lineNum

    elif eles[0] == 'OUT':
        index = int(eles[3]) - 1
        passenger_index = int(eles[1])
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_OPEN:
            return False, "PASSENGER OUT WHEN DOOR IS NOT OPEN!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "OUT WHEN RESET BEGIN!", lineNum
        if passenger_index not in passengers[index]:
            return False, "PASSENGER NOT IN ELEVATOR!", lineNum
        else:
            passengers[index].remove(passenger_index)
            allPassengers.pop(passenger_index)
        req = reqDict.get(passenger_index)
        if req == None:
            return False, "PASSENGER NOT EXIST!", lineNum
        else:
            req.setCurFloor(floors[index])
            req.setReceive(False)
            receives[index] = any(
                map(lambda x: x == index, allPassengers.values()))

    elif eles[0] == 'RECEIVE':
        passenger_index = int(eles[1])
        index = int(eles[2]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] == STATE_RESET_BEGIN:
            return False, "RECEIVE WHEN RESET BEGIN!", lineNum
        req = reqDict.get(passenger_index)
        if req == None:
            return False, "PASSENGER NOT EXIST!", lineNum
        else:
            if req.getReceive() == True:
                return False, "ONE RECEIVE MORE THAN ONCE", lineNum
            allPassengers[passenger_index] = index
            receives[index] = True
            req.setReceive(True)

    elif eles[0] == 'RESET_ACCEPT':
        index = int(eles[1]) - 1
        capacity = int(eles[2])
        speed = float(eles[3])
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        preSpeeds[index] = speed
        preCapacities[index] = capacity

    elif eles[0] == 'RESET_BEGIN':
        index = int(eles[1]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_CLOSE:
            return False, "RESET WHEN DOOR IS NOT CLOSE!", lineNum
        if preSpeeds[index] == -1 or preCapacities[index] == -1:
            return False, "RESET WITHOUT ACCEPT!", lineNum
        states[index] = STATE_RESET_BEGIN
        speeds[index] = preSpeeds[index]
        capacities[index] = preCapacities[index]
        lastResetTime[index] = opTime
        preCapacities[index] = -1
        preSpeeds[index] = -1

    elif eles[0] == 'RESET_END':
        index = int(eles[1]) - 1
        if not 0 <= index <= 5:
            return False, "UNKNOWN ELEVATOR ID!", lineNum
        if states[index] != STATE_RESET_BEGIN:
            return False, "RESET END WITHOUT BEGIN", lineNum
        if opTime - lastResetTime[index] < 1.2 - 0.00001:
        states[index] = STATE_CLOSE

    else:
        return False, "UNKNOWN OPTIONS!", lineNum

    return True, "Accepted", lineNum
