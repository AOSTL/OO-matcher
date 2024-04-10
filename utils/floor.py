from utils.params import *

class Floor:
    def __init__(self, floor) -> None:
        self.people = []
        self.floor = floor
        
    def addPerson(self, person, time = None):
        if time != None:
            person.latTime = time
        self.people.append(person)
    
    def popPerson(self, personID):
        for i in range(len(self.people)):
            if self.people[i].id == personID:
                return self.people.pop(i)
        raise Exception(f'Floor.popPerson: person {personID} not found')

    def receive(self, personid, elevatorid):
        for person in self.people:
            if person.id == personid:
                if person.ele != 0:
                    raise Exception(f'Floor.receive: person {personid} already received by elevator {person.ele}')
                person.ele = elevatorid
                return True
        return False
    
    def resetBegin(self, elevatorid):
        for person in self.people:
            if person.ele == elevatorid:
                person.ele = 0

    def check(self):
        MT = -10**9
        for person in self.people:
            if person.now != self.floor:
                raise Exception(f'Floor.check: person {person.id} not at the right floor')
            MT = max(MT, person.calcMT())
        return MT
        