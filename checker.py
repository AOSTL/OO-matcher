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
        self.ele_id = int(eles[6])

    def parseReq(self, req):
        req = req.replace('\n', '')
        index = req.index(']')
        req = req[index+1:]
        return req.split('-')

    def getUserId(self):
        return self.passenger_id

    def getFromFloor(self):
        return self.ff

    def getToFloor(self):
        return self.tf

    def getEleId(self):
        return self.ele_id

STATE_OPEN = 0
STATE_CLOSE = 1
MAX_FLOOR = 11
MIN_FLOOR = 1
MAX_NUM = 6
MIN_NUM = 0

reqDict = {}
floors = []
states = []
passengers = []
lastMoveTime = []
lastOpenTime = []
lastOpTime = []
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
                error.error_output(name, res[1], input_str, output_str, "Line: " + str(res[2]))
                return False

    if len(reqDict) != 0:
        missing = ""
        for req in reqDict.values():
            missing += str(req.getUserId()) + "\n"
        error.error_output(name, "Not all requests are processed", input_str, output_str, "Missing: " + missing)
        return False
    for i in range(6):
        if len(passengers[i]) != 0:
            error.error_output(name, "Someone is trapped in elevator", input_str, output_str, "Elevator ID: " + str(i + 1))
        if states[i] != STATE_CLOSE:
            error.error_output(name, "Elevator door is not close", input_str, output_str, "Elevator ID: " + str(i + 1))
            return False
    if flag[0] == 1:
        return True


def initElevator():
    reqDict.clear()
    floors.clear()
    states.clear()
    passengers.clear()
    lastMoveTime.clear()
    lastOpenTime.clear()
    lastOpTime.clear()
    flag[0] = 0
    for i in range(6):
        floors.append(1)
        states.append(STATE_CLOSE)
        passengers.append([])
        lastMoveTime.append(-10.0)
        lastOpenTime.append(-10.0)
        lastOpTime.append(0.0)

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
    opTime = float(read[1:index-1])
    read = read[index+1:]
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
        if opTime - lastMoveTime[index] < 0.4 - float(config["fault_tolerance"]):  # 小抖动误差
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
        passengers[index].append(passenger_index)
        req = reqDict.get(passenger_index)
        if req == None:
            return False, "PASSENGER NOT EXIST!", lineNum
        else:
            if req.getFromFloor() != int(eles[2]):
                return False, "IN MESSAGE NOT MATCH REQUEST!", lineNum
            if len(passengers[index]) > MAX_NUM:
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
        if passenger_index not in passengers[index]:
            return False, "PASSENGER NOT IN ELEVATOR!", lineNum
        else:
            passengers[index].remove(passenger_index)
        req = reqDict.get(passenger_index)
        if req == None:
            return False, "PASSENGER NOT EXIST!", lineNum
        else:
            if floors[index] != int(eles[2]):
                return False, "OUT MASSAGE NOT MATCH REQUEST!", lineNum
            reqDict.pop(passenger_index)

    else:
        return False, "UNKNOWN OPTIONS!", lineNum
    
    return True, "Accepted", lineNum
