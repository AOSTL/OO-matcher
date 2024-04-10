from utils.params import *
from utils.person import Person

# person = [time, id, start, end, ele, now]

class Elevator:
    def __init__(self, id):
        self.id = id
        self.minFloor = MIN_FLOOR
        self.maxFloor = MAX_FLOOR
        self.floor = 1
        self.person = []
        self.lastAction = [0, ACTION_ARRIVE, self.floor]
        self.carryLimit = ELE_CARRYLIMIT
        self.isOpen = False
        
        self.ele_move = ELE_MOVE_COST
        self.ele_open = ELE_OPEN_COST
        self.ele_close = ELE_CLOSE_COST
        self.ele_reset_cost = ELE_RESET_COST
        self.ele_reset_max = ELE_RESET_MAX
        
        self.resetAcceptTime = None
        self.resetBeginTime = None
        self.resetCarryLimit = None
        self.resetEleMove = None
        self.actionList = []
        self.receiveCnt = 0
    
    def addPerson(self, person: Person, time = None):
        if self.resetBeginTime != None:
            raise Exception(f'newPerson {person}: Elevator {self.id} is in reset')
        if time != None:
            person.lstTime = time
        if self.isOpen == False:
            raise Exception(f'newPerson {person}: Elevator {self.id} is not open')
        if self.id != person.ele:
            raise Exception(f'newPerson {person}: Elevator {self.id} is not the right elevator')
        if self.floor != person.now:
            raise Exception(f'newPerson {person}: Elevator {self.id} is not at the right floor')
        if len(self.person) >= self.carryLimit:
            raise Exception(f'newPerson {person}: Elevator {self.id} is full')
        if person.ele != self.id:
            raise Exception(f'newPerson {person}: Person {person.id} is not in the right elevator')
        self.person.append(person)
        
    def popPerson(self, personID):
        if self.resetBeginTime != None:
            raise Exception(f'popPerson: Elevator {self.id} is in reset')
        if self.isOpen == False:
            raise Exception(f'popPerson: Elevator {self.id} is not open')
        for i in range(len(self.person)):
            if self.person[i].id == personID:
                self.person[i].now = self.floor
                self.person[i].ele = 0
                self.receiveCnt -= 1
                return self.person.pop(i)
        raise Exception(f'popPerson: Elevator {self.id} person {personID} not found')
    
    def arrive(self, time, floor):
        if self.resetBeginTime != None:
            raise Exception(f'arrive: Elevator {self.id} is in reset')
        if self.receiveCnt == 0:
            raise Exception(f'arrive: Elevator {self.id} move when receiveCnt is 0')
        if self.isOpen:
            raise Exception(f'arrive: Elevator {self.id} is open')
        if abs(floor - self.floor) != 1:
            raise Exception(f'arrive: Elevator {self.id} floor {floor} is not next to {self.floor}')
        if floor < self.minFloor or floor > self.maxFloor:
            raise Exception(f'arrive: Elevator {self.id} floor {floor} is out of range')
        if time - self.lastAction[0] < self.ele_move - EPS:
            raise Exception(f'arrive: Elevator {self.id} move time {time - self.lastAction[0]} is less than {self.ele_move}')
        self.floor = floor
        self.lastAction = [time, ACTION_ARRIVE, self.floor]
        self.actionList.append(ACTION_ARRIVE)
    
    def open(self, time, floor):
        if self.resetBeginTime != None:
            raise Exception(f'open: Elevator {self.id} is in reset')
        if self.isOpen:
            raise Exception(f'open: Elevator {self.id} is open')
        if self.floor != floor:
            raise Exception(f'open: Elevator {self.id} floor {floor} is not at {self.floor}')
        self.isOpen = True
        self.lastAction = [time, ACTION_OPEN, self.floor]
        self.actionList.append(ACTION_OPEN)
        
    def close(self, time, floor):
        if self.resetBeginTime != None:
            raise Exception(f'close: Elevator {self.id} is in reset')
        if self.isOpen == False:
            raise Exception(f'close: Elevator {self.id} is not open')
        if self.floor != floor:
            raise Exception(f'close: Elevator {self.id} floor {floor} is not at {self.floor}')
        if time - self.lastAction[0] < self.ele_open + self.ele_close - EPS:
            raise Exception(f'close: Elevator {self.id} open and close time {time - self.lastAction[0]} is less than {self.ele_open + self.ele_close}')
        self.isOpen = False
        self.lastAction = [time, ACTION_CLOSE, self.floor]
        self.actionList.append(ACTION_CLOSE)
    
    def resetAccept(self, time, carryLimit, eleMove):
        if self.resetAcceptTime != None:
            raise Exception(f'Elevator.resetAccept: Elevator {self.id} is already in reset accept')
        if self.resetBeginTime != None:
            raise Exception(f'Elevator.resetAccept: Elevator {self.id} is already in reset begin')
        self.resetAcceptTime = time
        self.resetCarryLimit = carryLimit
        self.resetEleMove = eleMove
        self.actionList = [ACTION_RESET_ACCEPT]
        
    def resetBegin(self, time):
        if self.resetAcceptTime == None:
            raise Exception(f'Elevator.resetBegin: Elevator {self.id} is not in reset accept')
        if self.resetBeginTime != None:
            raise Exception(f'Elevator.resetBegin: Elevator {self.id} is already in reset begin')
        if self.person != []:
            raise Exception(f'Elevator.resetBegin: Elevator {self.id} is not empty')
        if self.isOpen:
            raise Exception(f'Elevator.resetBegin: Elevator {self.id} is open')
        if self.actionList.count(ACTION_ARRIVE) > 2:
            raise Exception(f'Elevator.resetBegin: Elevator {self.id} arrive too many times')
        self.resetBeginTime = time
        self.carryLimit = self.resetCarryLimit
        self.ele_move = self.resetEleMove
        self.actionList.append(ACTION_RESET_BEGIN)
        
    def resetEnd(self, time):
        if self.resetAcceptTime == None:
            raise Exception(f'Elevator.resetEnd: Elevator {self.id} is not in reset accept')
        if self.resetBeginTime == None:
            raise Exception(f'Elevator.resetEnd: Elevator {self.id} is not in reset begin')
        if time - self.resetBeginTime < self.ele_reset_cost - EPS:
            raise Exception(f'Elevator.resetEnd: Elevator {self.id} reset time {time - self.resetBeginTime} is less than {self.ele_reset_cost}')
        if time - self.resetAcceptTime > self.ele_reset_max + EPS:
            raise Exception(f'Elevator.resetEnd: Elevator {self.id} reset time {time - self.resetAcceptTime} is more than {self.ele_reset_max}')
        if self.actionList.count(ACTION_ARRIVE) > 2:
            raise Exception(f'Elevator.resetEnd: Elevator {self.id} arrive too many times')
        self.resetBeginTime = None
        self.resetAcceptTime = None
        self.carryLimit = self.resetCarryLimit
        self.ele_move = self.resetEleMove
        self.lastAction = [time, ACTION_RESET_END, self.id]
        

    def check(self):
        if self.person != []:
            raise Exception(f'Elevator.check: Elevator {self.id} people not empty')
        if self.isOpen == True:
            raise Exception(f'Elevator.check: Elevator {self.id} is open')
        if self.resetAcceptTime != None:
            raise Exception(f'Elevator.check: Elevator {self.id} is in reset state')
        return True


