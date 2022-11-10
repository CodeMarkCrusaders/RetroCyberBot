import sys
import os
import json
sys.path.append(os.path.dirname(sys.path[0]))
from Thing.Thing import GetBuff

p = 'buff_list'
def GetData(path):

    with open(path, encoding ='utf-8') as outfile:
        data : list = json.load(outfile)

    return GetBuff(data)

all_buff = {}
def g(f):
    for root, dirs, files in os.walk(f):  
        if '__pycache__' in root :
            continue
        for buff_paht in files:
            if buff_paht in ['buff.py']:
                continue
            all_buff[buff_paht.split('.')[0]] = GetData(root +'\\'+ buff_paht)
            

g(p)
print(1)