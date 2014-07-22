import json
import requests
from datadiff.tools import assert_equal

def getKeyName(obj):
    if type(obj) is dict:
        return 'dict'
    elif type(obj) is list:
        return 'list'
    elif type(obj) is str:
        return obj
    else:
        return str(obj)


def norm(incoming):
    if type(incoming) is dict:
        return {key: norm(value) for key, value in sorted(incoming.iteritems())}
    elif type(incoming) is list:
        return {getKeyName(key): norm(key) for key in sorted(incoming)}
    else:
        return ''

def main():
    r = requests.get("https://raw.githubusercontent.com/vz-risk/veris/master/verisc-labels.json")
    labels = json.loads(r.text or r.content)
    r = requests.get("https://raw.githubusercontent.com/vz-risk/veris/master/verisc-enum.json")
    enum = json.loads(r.text or r.content)
    assert_equal(norm(enum),norm(labels),msg='Differences Found')


if __name__ == '__main__':
    main()
