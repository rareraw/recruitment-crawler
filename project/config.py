import json
import os


class Config:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    configJson = json.load(open(ROOT_DIR + '/.projectconfig', 'r'))

    @staticmethod
    def get(find_key):
        keys = find_key.split('.')
        val = Config.configJson
        for key in keys:
            val = val[key]
        return val
