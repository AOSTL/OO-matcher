from utils.params import *

# person = [time, id, start, end, now]

class Person:
    def __init__(self, person):
        self.time = person[0]
        self.id = person[1]
        self.start = person[2]
        self.end = person[3]
        self.now = person[4]
        self.ele = 0
        self.lstTime = self.time
    
    def calcET(self):
        res = 0
        for f in range(MIN_FLOOR, MAX_FLOOR + 1):
            res += abs(self.start - f) * ELE_MOVE_COST
        res /= MAX_FLOOR - MIN_FLOOR + 1
        res += ELE_OPEN_COST + ELE_CLOSE_COST + abs(self.start - self.end) * ELE_MOVE_COST
        return res
    
    def calcMT(self):
        return self.lstTime - self.time - self.calcET()
    
    def __str__(self):
        return f'[{self.time}]{self.id}-FROM-{self.start}-TO-{self.end}-BY-{self.ele}'
    
