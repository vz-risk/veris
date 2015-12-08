import json
from collections import defaultdict

with open("./verismm_skill_tree.json", "r") as file_handle:
    verismm = json.load(file_handle)

def parse_verismm(d, skill):
    ret = defaultdict(dict)
    for k, v in d[u"Skills"].iteritems():
        if v:
            tmp_ret = parse_verismm(v, k)
            for k, v in tmp_ret.iteritems():
                ret[k].update(v)
    if u'Record' in d:
        l = list()
        for k, v in d[u'Record'].iteritems():
            if v is None:
                l.append("{0}: all".format(k))
            elif type(v) == str or type(v) == unicode:
                l.append("{0}: {1}".format(k, v))
            elif type(v) == list:
                l.append("{0}: some".format(k))
            else:
                l.append(k)
        ret[d[u'Level']].update({skill: l})
    return ret

skills = parse_verismm(verismm, "")

for level in skills:
    print "Level {0}".format(level)
    for skill in skills[level]:
        print "  * {0}".format(skill)
        for record in skills[level][skill]:
            print "    * {0}".format(record)