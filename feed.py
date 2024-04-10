import time

if __name__ == '__main__':
    '''
    读入：多行，每行为[时间戳]str，以EOF为结束
    时间戳精确到小数点后一位，以s为单位
    输出：按时间定时输出str
    如：输入[4.3]str，则在4.3s时输出str
    '''
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    now = 0
    for line in lines:
        curTime = int(float(line[1:line.find(']')]) * 10)
        time.sleep(max(0, (curTime - now) / 10))
        print(line[line.find(']') + 1:])
        now = curTime
        
