import json
from pathlib import Path
config = {}


def setConfig(k, v):
    config[k] = v


def getConfig():
    return config


def getData(name):
    fname = name
    if not name.endswith('.json'):
        fname = f"{fname}.json"
    target_dir = Path('../data/json')
    with open(target_dir / fname) as f:
        return json.load(f)