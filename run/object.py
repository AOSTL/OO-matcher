class PASSANGER:
    def __init__(self, id, from_floor, to_floor):
        self.id = id
        self.at_floor = from_floor
        self.to_floor = to_floor
        self.received = False

class ELEVATOR:
    def __init__(self, id):
        self.id = id
        self.current_floor = 1
        self.capacity = 6
        self.speed = 0.4
        self.open_close_time = 0.4
        self.last_action_time = -10
        self.door_status = False
        self.passangers = []
        self.waiting_passangers = []
        self.reset_begin = False
        self.reset_scheduled = False
        self.reset_action = None
        self.reset_arrive_count = 0
        self.reset_gap = 5.0

    def add_passanger(self, passanger):
        self.passangers.append(passanger)

    def remove_passanger(self, passanger):
        self.passangers.remove(passanger)

    def add_waiting_passanger(self, passanger):
        self.waiting_passangers.append(passanger)

    def remove_waiting_passanger(self, passanger):
        self.waiting_passangers.remove(passanger)

class ACTION:
    def __init__(self, time, type):
        self.time = time
        self.type = type

class arrive(ACTION):
    def __init__(self, time, type, floor, id):
        super().__init__(time, type)
        self.floor = floor
        self.elevator = id

class open(ACTION):
    def __init__(self, time, type, floor, id):
        super().__init__(time, type)
        self.floor = floor
        self.elevator = id

class close(ACTION):
    def __init__(self, time, type, floor, id):
        super().__init__(time, type)
        self.floor = floor
        self.elevator = id

class passanger_in(ACTION):
    def __init__(self, time, type, passanger, floor, id):
        super().__init__(time, type)
        self.floor = floor
        self.elevator = id
        self.passanger = passanger

class passanger_out(ACTION):
    def __init__(self, time, type, passanger, floor, id):
        super().__init__(time, type)
        self.floor = floor
        self.elevator = id
        self.passanger = passanger

class passanger_receive(ACTION):
    def __init__(self, time, type, passanger, id):
        super().__init__(time, type)
        self.elevator = id
        self.passanger = passanger

class reset_accepted(ACTION):
    def __init__(self, time, type, id, capacity, speed):
        super().__init__(time, type)
        self.elevator = id
        self.capacity = capacity
        self.speed = speed

class reset_begin(ACTION):
    def __init__(self, time, type, id):
        super().__init__(time, type)
        self.elevator = id
        
class reset_end(ACTION):
    def __init__(self, time, type, id):
        super().__init__(time, type)
        self.elevator = id