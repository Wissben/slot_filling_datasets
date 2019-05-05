import os
import json
from pprint import pprint as pr
import re


def make_ids(intents):
    for id, intent in enumerate(intents):
        intent['id'] = id+1
    # pr(data)


def fill_placeholders(intents, plugs):
    new = []
    start_id = 1
    for plug in plugs:
        for intent in intents:
            text = intent['text']
            text = re.sub(r'{(.+?):}', r'{\1:'+plug+'}', text)
            obj_model = {'id': start_id, 'text': text,
                         'intent': intent['intent']}
            # pr(obj_model)
            new.append(obj_model)
            start_id += 1
            if(start_id % 1000 == 0):
                pr(start_id)
    return new


def exclude_condition(dir):
    conds = [
        dir not in ['lib', 'bin', 'logs', 'log'],
        not dir.startswith('.'),
        not dir.startswith('_'),
        not dir.startswith('-')
    ]

    return all(conds)


def get_sub_dirs(path):
    folders = []
    # r=root, d=directories, f = files
    for r, dirnames, f in os.walk(path):
        dirnames = [dir for dir in dirnames if exclude_condition(dir)]
        for folder in dirnames:
            folders.append(folder)
            # print(folder)
    return folders


# "/home/weiss/Documents/intent_parser/train_intents.json"
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'train_intents.json')
# "/home/weiss/Documents/intent_parser/train_intents_cleaned.json"
DATASET_CLEANED_PATH = os.path.join(
    os.path.dirname(__file__), 'train_intents_cleaned.json')
ROOT_PATH = '/home/weiss/CODES'
PLUGS = get_sub_dirs(ROOT_PATH)
pr(len(PLUGS))

try:
    fd = open(DATASET_PATH, 'r')
    f = open(DATASET_CLEANED_PATH, 'w')
    data = json.load(fd)
    data['train_dataset']['folders'] = fill_placeholders(
        data['train_dataset']['folders'], PLUGS)
    data['train_dataset']['files'] = fill_placeholders(
        data['train_dataset']['files'], PLUGS)
    make_ids(data['train_dataset']['folders'])
    make_ids(data['train_dataset']['files'])
    json.dump(data, f, indent=4, separators=(',', ': '))
except FileNotFoundError as e:
    pr('[ERROR] : ', e)
