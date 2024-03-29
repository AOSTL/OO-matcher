import random
import json

config=json.load(open('config.json','r',encoding='utf-8'))

def generate_input():
    idlist=list(range(1,101))
    for i in range(0,10):
        idlist.append(random.randint(101,999999999))
    random.shuffle(idlist)

    command_num=random.randint(1,int(config["command_limit"]))
    time_limit=float(config["time_limit"])
    ans=[]
    for i in range(0,command_num):
        thistime=random.random()*(time_limit-1)+1
        afrom=int(0)
        to=int(0)
        while afrom==to:
            afrom=random.randint(int(config["min_floor"]),int(config["max_floor"]))
            to=random.randint(int(config["min_floor"]),int(config["max_floor"]))
        elevator=random.randint(1,int(config["elevator_num"]))

        string='['+format(thistime,'.1f')+']'+str(idlist[i])+'-FROM-'+str(afrom)+'-TO-'+str(to)+'-BY-'+str(elevator)
        ans.append([thistime,string])

    #按thistime从小到大排序
    ans.sort(key=lambda x:x[0])
    return ans, command_num