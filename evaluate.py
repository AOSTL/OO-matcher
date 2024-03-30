import run_java
import re
import json
import error
from functools import lru_cache
import os
import func_timeout

config=json.load(open('config.json','r',encoding='utf-8'))

def evaluate(origin, name):
    if (os.name == 'nt'):
        program_path = '.\\tools\\datainput_student_win64.exe'
    else:
        program_path = './tools/datainput_student_linux_x86_64'
    output = ""
    run_time = 0
    try:
        output, run_time = run_java.execute_java_with_program(name, program_path)
    except func_timeout.exceptions.FunctionTimedOut as e:
        error.error_output(name, "Time Limit Exceeded", origin, "", e)
        return False, 0
    waiters = get_waiters(origin)
    return check(output, waiters, name, origin), run_time

def get_waiters(origin):
    command_num = origin.count('\n')
    lines = origin.split('\n')
    waiters=[{} for i in range(0, int(config["elevator_num"]))]
    for i in range(0, command_num):
        matcher=re.match(r'\[\s*(\d+\.\d+)\](\d+)-FROM-(\d+)-TO-(\d+)-BY-(\d+)', lines[i])
        id=int(matcher.group(2))
        afrom=int(matcher.group(3))
        to=int(matcher.group(4))
        thistime=float(matcher.group(1))
        elevator=int(matcher.group(5))
        waiters[elevator-1][id]=[afrom,to,thistime]
    return waiters


def check(output, waiters, name, origin):
    index_line=0
    index_time=1
    index_command=2
    index_floor=3
    index_elevator=4
    index_passenger=5
    lines = output.replace('\r', '').split('\n')
    info=[[], [], [], [], [], []] #电梯i的第几行、时间、指令、楼层、电梯id(、乘客id)
    for i in range(0,len(lines)):
        line=[i+1]
        matcher=re.match(r'\[\s+(\d+\.\d+)\]([A-Z]*)-(\d+)-(\d+)-?(.*)',lines[i])
        try:
            line.append(float(matcher.group(1)))
            line.append(matcher.group(2))
            if matcher.group(5)!='':
                line.append(int(matcher.group(4)))
                line.append(int(matcher.group(5)))
                line.append(int(matcher.group(3)))
            else:
                line.append(int(matcher.group(3)))
                line.append(int(matcher.group(4)))
            info[line[index_elevator]-1].append(line)
            if line[index_elevator]>6 or line[index_elevator]<1:
                error.error_output(name, "Elevator Error", origin, output, '第 ' + str(i + 1) + ' 行不存在的电梯')
                return False
        except:
            error.error_output(name, "Format Error", origin, output, '第 '+str(i+1)+' 行格式错误')
            return False
        if line[index_command] not in ['ARRIVE','OPEN','CLOSE','IN','OUT']:
            error.error_output(name, "Command Error", origin, output, '第 '+str(i+1)+' 行指令错误')
            return False

    for i in range(0,6):    #电梯数量
        passenger={}    #电梯内的人
        waiter=waiters[i]   #等待的人
        last_arrive_time=0  #上次到达的时间
        last_arrive_floor=int(config["default_floor"]) #上次到达的楼层
        last_open_time=0    #上次开门的时间
        last_close_time=1e-9    #上次关门的时间
        is_open = False #是否开门
        reason=''
        for j in range(0,info[i].__len__()):
            command=info[i][j][index_command]
            if command=='ARRIVE':
                arrive_floor=info[i][j][index_floor]
                if abs(arrive_floor-last_arrive_floor)!=1 or arrive_floor<1 or arrive_floor>11:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'楼层错误'
                    error.error_output(name, "Invalid Floor", origin, output, reason)
                    break
                if info[i][j][index_time]-last_arrive_time<float(config["move_time"])-float(config["fault_tolerance"]):
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'到达时间错误'
                    error.error_output(name, "Time Error", origin, output, reason)
                    break
                if is_open == True:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'没关门就跑了'
                    error.error_output(name, "run when open", origin, output, reason)
                    break

                last_arrive_time=info[i][j][index_time]
                last_arrive_floor=arrive_floor
            elif command=='OPEN':
                if last_arrive_floor!=info[i][j][index_floor]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'还没到这个楼层'
                    error.error_output(name, "Floor Error", origin, output, reason)
                    break
                if is_open == True:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'只有关门后才能开门'
                    error.error_output(name, "Door Open Before Close", origin, output, reason)
                    break
                is_open = True
                last_open_time=info[i][j][index_time]
            elif command=='CLOSE':
                if last_arrive_floor!=info[i][j][index_floor]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'还没到这个楼层'
                    error.error_output(name, "Floor Error", origin, output, reason)
                    break
                if is_open == False:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'只有开门后才能关门'
                    error.error_output(name, "Door Close Before Open", origin, output, reason)
                    break
                if info[i][j][index_time]-last_open_time<float(config["open_time"])+float(config["close_time"])-float(config["fault_tolerance"]):
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'关门时间错误'
                    error.error_output(name, "Door Close Time Error", origin, output, reason)
                    break
                is_open=False
                last_close_time=info[i][j][index_time]
            elif command=='IN':
                if last_arrive_floor!=info[i][j][index_floor]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'还没到这个楼层'
                    error.error_output(name, "Passanger Entered NULL Elevator", origin, output, reason)
                    break
                if is_open == False:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'门还没开'
                    error.error_output(name, "Passanger Entered Before Door Open", origin, output, reason)
                    break
                if passenger.__len__()>=int(config["max_capacity"]):
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'超载了'
                    error.error_output(name, "Overload", origin, output, reason)
                    break
                if info[i][j][index_passenger] not in waiter.keys():
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'上错人了'
                    error.error_output(name, "Passanger Entered Wrong Elevator", origin, output, reason)
                    break
                if info[i][j][index_floor]!=waiter[info[i][j][index_passenger]][0]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'：正确的人，但不在此层上'
                    error.error_output(name, "Passanger At Wrong Floor", origin, output, reason)
                    break
                if info[i][j][index_time]<waiter[info[i][j][index_passenger]][2] - float(config["fault_tolerance"]):
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'：正确的人，但人还没到'
                    error.error_output(name, "Passanger Entered Too Early", origin, output, reason)
                    break
                passenger[info[i][j][index_passenger]]=waiter[info[i][j][index_passenger]]
                waiter.pop(info[i][j][index_passenger])
            elif command=='OUT':
                if last_arrive_floor!=info[i][j][index_floor]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'还没到这个楼层'
                    error.error_output(name, "Passanger Exited NULL Elevator", origin, output, reason)
                    break
                if is_open==False:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'门还没开'
                    error.error_output(name, "Passanger Exited Before Door Open", origin, output, reason)
                    break
                if info[i][j][index_passenger] not in passenger.keys():
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'走出了不存在的人'
                    error.error_output(name, "NULL Passanger Exited", origin, output, reason)
                    break
                if info[i][j][index_floor]!=passenger[info[i][j][index_passenger]][1]:
                    reason='第'+str(info[i][j][index_line])+'行电梯'+str(i+1)+'正确的人，但不在此层下'
                    error.error_output(name, "Passanger Exited At Wrong Floor", origin, output, reason)
                    break
                passenger.pop(info[i][j][index_passenger])
        # print(origin)
        # print(output)
        # # print(output)
        # print(is_open)
        # print(passenger.__len__())
        # print(waiter.__len__())
        # print(reason)
        if reason=='' and is_open==True:
            print("1")
            reason='第'+str(info[i][info[i].__len__()-1][index_line])+'行电梯'+str(i+1)+'记得要关门'
            error.error_output(name, "Door Close Before Open", origin, output, reason)
        if reason=='' and passenger.__len__()>0:
            print("2")
            reason='第'+str(info[i][info[i].__len__()-1][index_line])+'行电梯'+str(i+1)+'里的乘客还没出来'
            error.error_output(name, "Passanger Not Exited", origin, output, reason)
        if reason=='' and waiter.__len__()>0:
            print("3")
            reason='第'+str(info[i][info[i].__len__()-1][index_line])+'行电梯'+str(i+1)+'还没运送完乘客'
            error.error_output(name, "Passanger Not Transported", origin, output, reason)
        if reason!='':
            break

    if reason!='':
        return False
    else:
        return True