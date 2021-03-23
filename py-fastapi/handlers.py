import json
from pathlib import Path


config = {"jsonDir": Path("../data/json")}


def setConfig(k, v):
    config[k] = v


def getConfig():
    return config


def getJsonFromFile(name):
    fname = name
    if not name.endswith(".json"):
        fname = f"{fname}.json"
    with open(config["jsonDir"] / fname) as f:
        return json.load(f)
