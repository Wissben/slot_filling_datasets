import os
import json
from pprint import pprint as pr
import re 


def make_ids(intents):
    for id,intent in enumerate(intents):
        intent['id']=id+1
    # pr(data)


def fill_placeholders(intents,plugs):
    new = []
    start_id = 1
    for plug in plugs:
        for intent in intents:
            text = intent['text']
            text = re.sub(r'{(.+?):}',r'{\1:'+plug+'}',text)
            obj_model = {'id':start_id,'text':text,'intent':intent['intent']}
            pr(obj_model)
            new.append(obj_model)
            start_id +=1
    intents = new

def exclude_condition(dir):
    conds = [
        dir not in ['lib','bin','logs','log'],
        not dir.startswith('.'),
        not dir.startswith('_'),
        not dir.startswith('-')
        ]

    return all(conds)

def get_sub_dirs(path):
    folders = []
    # r=root, d=directories, f = files
    for r, dirnames, f in os.walk(path):
        dirnames =[dir for dir in dirnames if exclude_condition(dir)]
        for folder in dirnames:
            folders.append(folder)
            print(folder)
    return folders



DATASET_PATH = "/home/weiss/Documents/intent_parser/train_intents.json"
ROOT_PATH = '/home/weiss/Tools'
PLUGS = get_sub_dirs(ROOT_PATH)
pr(PLUGS)

try:
    fd = open(DATASET_PATH,'r')
    data = json.load(fd)
    fill_placeholders(data['train_dataset']['folders'],PLUGS)
    make_ids(data['train_dataset']['folders'])
except FileNotFoundError as e:
    pr('[ERROR] : ',e)
