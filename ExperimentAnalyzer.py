import os
from optparse import OptionParser
from pprint import pprint

import numpy as np

import AnalyzeResults


def analyze(dirpath):
    query = []
    results = []
    complatency = []
    e2elat = []
    cache = []
    for node in os.listdir(dirpath):
        node = dirpath + os.sep + node
        q, r, c, e, ca = AnalyzeResults.parse(node)
        query.extend(q)
        results.extend(r)
        complatency.extend(c)
        e2elat.extend(e)
        cache.extend(ca)
    return {"precision": AnalyzeResults.precision(query, results),
            "recall": AnalyzeResults.recall(query, results),
            "complatency": AnalyzeResults.avglatency(complatency),
            "e2elatency": AnalyzeResults.avglatency(e2elat),
            "cache": AnalyzeResults.avgCachehits(cache)}


def analyze_bat(dirpath):
    bat = []
    for node in os.listdir(dirpath):
        node = dirpath + os.sep + node
        bat.append(AnalyzeResults.battery(node))

    return np.mean(bat)


def analyze_iters(dirpath):

    exp = {"precision": [],
            "recall": [],
            "complatency": [],
            "e2elatency": [],
            "cache": [],
            "battery": []}
    for iteration in os.listdir(dirpath):
        iteration = dirpath + os.sep + iteration
        log = iteration + os.sep + "logs"
        ret = analyze(log)
        for k in ret:
            exp[k].append(ret[k])

        batdir = iteration + os.sep + "trepn"
        exp["battery"].append(analyze_bat(batdir))

    for k in exp:
        vals = exp[k]
        exp[k] = (np.mean(exp[k]), np.std(exp[k]))

    return exp

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--crowdinput", type="str", dest="cpath", help="Crowd Input Dir")
    parser.add_option("-s", "--serverinput", type="str", dest="spath", help="Server Input Dir")
    parser.add_option("-e", "--exp", type="str", dest="epath", help="Experiment Input Dir")

    (options, args) = parser.parse_args()

    if options.epath is None:
        print("Crowd:")
        pprint(analyze(options.cpath))
        print("Server:")
        pprint(analyze(options.spath))
    else:
        print("Crowd:")
        pprint(analyze_iters(options.epath + os.sep + "Crowd"))# + os.sep + "logs"))
        print("Server:")
        pprint(analyze_iters(options.epath + os.sep + "Server"))# + os.sep + "logs"))
