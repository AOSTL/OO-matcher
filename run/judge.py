from run.object import ELEVATOR, PASSANGER
import json

config = json.load(open('config.json','r',encoding='utf-8'))

def judge(passangers, actions):
    elevators = [ELEVATOR(i + 1) for i in range(7)]
    i = 0
    for action in actions:
        res = []
        i = i + 1
        elevator = elevators[action.elevator - 1]
        match action.type:
            case 'ARRIVE':
                res = _judge_arrive(elevator, action)
            case 'OPEN':
                res = _judge_open(elevator, action)
            case 'CLOSE':
                res = _judge_close(elevator, action)
            case 'IN':
                res = _judge_in(elevator, action, passangers)
            case 'OUT':
                res = _judge_out(elevator, action, passangers)
            case 'RECEIVE':
                res = _judge_receive(elevator, action, passangers)
            case 'RESET_ACCEPT':
                res = _judge_reset_accept(elevator, action)
            case 'RESET_BEGIN':
                res = _judge_reset_begin(elevator, action, passangers)
            case 'RESET_END':
                res = _judge_reset_end(elevator, action)
        if res[0] == False:
            return res[0], res[1], 'Line ' + str(i) + ': [' + str(action.time) + ']'
    
    for elevator in elevators:
        if elevator.passangers:
            return False, 'Elevator' + str(elevator.id) + ' End With Passanger', str(str(elevator.id))
        elif elevator.door_status != False:
            return False, 'Elevator' + str(elevator.id) + ' End With Door open', str(str(elevator.id))
        elif elevator.waiting_passangers:
            return False, 'Elevator' + str(elevator.id) + ' End With Waiting Passanger', str(elevator.id)

    for passanger in passangers.values():
        if passanger.at_floor != passanger.to_floor:
            return False, 'Passanger End Not Arrived', str(passanger.id)
    
    return True, '', ''


def _judge_arrive(elevator, action):
    if elevator.door_status == True:
        return False, 'Elevator' + str(elevator.id) + ' Move With Door open'
    elif elevator.waiting_passangers.__len__() == 0 and elevator.passangers.__len__() == 0:
        return False, 'Elevator' + str(elevator.id) + ' Move With No Passanger In Elevator or Waiting'
    elif abs(elevator.current_floor - action.floor) > 1:
        return False, 'Elevator' + str(elevator.id) + ' Move 1+ Floors At Once'
    elif action.floor < 1 or action.floor > 11:
        return False, 'Elevator' + str(elevator.id) + ' Move To Invalid Floor'
    elif action.time - elevator.last_action_time + config['fault_tolerance'] < elevator.speed:
        return False, 'Elevator' + str(elevator.id) + ' Over Speed'
    elif elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Move During Reset'
    elevator.current_floor = action.floor
    elevator.last_action_time = action.time
    elevator.reset_arrive_count = elevator.reset_arrive_count + 1
    return True, ''

def _judge_open(elevator, action):
    if elevator.door_status == True:
        return False, 'Elevator' + str(elevator.id) + ' Open Door While Door Already Open'
    elif elevator.current_floor != action.floor:
        return False, 'Elevator' + str(elevator.id) + ' Open Door At Wrong Floor'
    elif elevator.waiting_passangers.__len__() == 0 and elevator.passangers.__len__() == 0:
        return False, 'Elevator' + str(elevator.id) + ' Open Door With No Passanger In Elevator or Waiting'
    elif elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Open Door During Reset'
    elevator.door_status = True
    elevator.last_action_time = action.time
    return True, ''

def _judge_close(elevator, action):
    if elevator.door_status == False:
        return False, 'Elevator' + str(elevator.id) + ' Close Door While Door Already Close'
    elif elevator.current_floor != action.floor:
        return False, 'Elevator' + str(elevator.id) + ' Close Door At Wrong Floor'
    elif elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Close Door During Reset'
    elif action.time - elevator.last_action_time + config["fault_tolerance"] < elevator.open_close_time:
        return False, 'Elevator' + str(elevator.id) + ' Over Speed'
    elevator.door_status = False
    elevator.last_action_time = action.time
    return True, ''

def _judge_in(elevator, action, passangers):
    if passangers[action.passanger] == None:
        return False, 'Elevator' + str(elevator.id) + ' In Non-Existent Passanger'
    elif passangers[action.passanger].at_floor != elevator.current_floor:
        return False, 'Elevator' + str(elevator.id) + ' Passanger Not At Floor'
    elif action.floor != elevator.current_floor:
        return False, 'Elevator' + str(elevator.id) + ' In Passanger At Wrong Floor'
    elif elevator.door_status == False:
        return False, 'Elevator' + str(elevator.id) + ' In Passanger While Door Close'
    elif elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' In Passanger During Reset'
    elif elevator.passangers.__len__() == elevator.capacity:
        return False, 'Elevator' + str(elevator.id) + ' In Passanger While Full'
    elif action.passanger not in elevator.waiting_passangers:
        return False, 'Elevator' + str(elevator.id) + ' In Passanger Not In Waiting List'
    elevator.remove_waiting_passanger(action.passanger)
    elevator.add_passanger(action.passanger)
    return True, ''

def _judge_out(elevator, action, passangers):
    if passangers[action.passanger] == None:
        return False, 'Elevator' + str(elevator.id) + ' Out Non-Existent Passanger'
    elif action.floor != elevator.current_floor:
        return False, 'Elevator' + str(elevator.id) + ' Out Passanger At Wrong Floor'
    elif elevator.door_status == False:
        return False, 'Elevator' + str(elevator.id) + ' Out Passanger While Door Close'
    elif elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Out Passanger During Reset'
    elif action.passanger not in elevator.passangers:
        return False, 'Elevator' + str(elevator.id) + ' Out Passanger Not In Elevator'
    passangers[action.passanger].at_floor = elevator.current_floor
    passangers[action.passanger].received = False
    elevator.remove_passanger(action.passanger)
    return True, ''

def _judge_receive(elevator, action, passangers):
    if elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Receive Passanger During Reset'
    elif passangers[action.passanger] == None:
        return False, 'Elevator' + str(elevator.id) + ' Receive Non-Existent Passanger'
    elif passangers[action.passanger].received == True:
        return False, 'Elevator' + str(elevator.id) + ' Receive Passanger Already Received'
    elevator.add_waiting_passanger(action.passanger)
    passangers[action.passanger].received = True
    return True, ''

def _judge_reset_accept(elevator, action):
    if elevator.reset_begin == True:
        return False, 'Elevator' + str(elevator.id) + ' Accept Reset During Reset'
    elevator.reset_action = action
    elevator.reset_scheduled = True
    elevator.reset_arrive_count = 0
    return True, ''

def _judge_reset_begin(elevator, action, passangers):
    if elevator.door_status == True:
        return False, 'Elevator' + str(elevator.id) + ' Begin Reset While Door Open'
    elif elevator.passangers.__len__() > 0:
        return False, 'Elevator' + str(elevator.id) + ' Begin Reset With Passanger'
    elif elevator.reset_scheduled == False:
        return False, 'Elevator' + str(elevator.id) + ' Unauthorized Reset'
    elif elevator.reset_arrive_count > 2:
        return False, 'Elevator' + str(elevator.id) + ' Begin Reset After Arriving 2+ Floors'
    for passanger in elevator.waiting_passangers:
        passangers[passanger].received = False
    elevator.waiting_passangers = []
    elevator.reset_begin = True
    elevator.reset_scheduled = False
    elevator.last_action_time = action.time
    return True, ''


def _judge_reset_end(elevator, action):
    if elevator.reset_begin == False:
        return False, 'Elevator' + str(elevator.id) + ' End Reset Without Begin'
    elif action.time - elevator.reset_action.time > elevator.reset_gap + config["fault_tolerance"]:
        return False, 'Elevator' + str(elevator.id) + ' End Reset After Idle Time'
    elif action.time - elevator.last_action_time + config["fault_tolerance"] < 1.2:
        return False, 'Elevator' + str(elevator.id) + ' End Reset Before Idle Time'
    elevator.capacity = elevator.reset_action.capacity
    elevator.speed = elevator.reset_action.speed
    elevator.reset_begin = False
    elevator.last_action_time = action.time
    return True, ''