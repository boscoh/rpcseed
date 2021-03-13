import json
from pathlib import Path


config = {"target_dir": Path("../data/json")}


def setConfig(k, v):
    config[k] = v


def getConfig():
    return config


def getDataFromJson(name):
    fname = name
    if not name.endswith(".json"):
        fname = f"{fname}.json"
    with open(config["target_dir"] / fname) as f:
        return json.load(f)
