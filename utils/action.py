class Action:
    '''
    action = [时间戳, 动作, 位置, 电梯ID] | [时间戳, 动作, 位置, 电梯ID, 乘客ID]
                | [时间戳, 动作, 电梯ID] | [时间戳, 动作, 电梯ID, 乘客ID]
                | [时间戳, 动作, 电梯ID, 满载人数, 移动一层时间]
    '''
    def __init__(self, time, action, *args):
        self.time = time
        self.action = action
        self.args = args
