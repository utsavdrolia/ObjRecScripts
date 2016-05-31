import os
from optparse import OptionParser
from pprint import pprint

import numpy as np

import AnalyzeResults


def get_cache_hits(resultpath):
    resulttuple = zip(*AnalyzeResults.parse(resultpath))
    complatency = []
    latency = []
    query = []
    result = []
    for q, r, complat, overalllat, cachehits in resulttuple:
        if cachehits == 1:
            complatency.append(complat)
            latency.append(overalllat)
            query.append(q)
            result.append(r)

    return query, result, complatency, latency


def get_cache_hits_nodes(nodedir):
    complatency = []
    latency = []
    query = []
    result = []
    nodes = os.listdir(nodedir)
    for node in nodes:
        node = nodedir + os.sep + node
        q, r, complat, overalllat = get_cache_hits(node)
        complatency.extend(complat)
        latency.extend(overalllat)
        query.extend(q)
        result.extend(r)

    return query, result, complatency, latency


def analyze_iters(dirpath):
    exp = {"precision": [],
            "recall": [],
            "complatency": [],
            "e2elatency": []}
    for iteration in os.listdir(dirpath):
        iteration = dirpath + os.sep + iteration
        query, results, complatency, e2elat = get_cache_hits_nodes(iteration)
        exp["precision"].append(AnalyzeResults.precision(query, results))
        exp["recall"].append(AnalyzeResults.recall(query, results))
        exp["complatency"].append(AnalyzeResults.avglatency(complatency))
        exp["e2elatency"].append(AnalyzeResults.avglatency(e2elat))

    for k in exp:
        vals = exp[k]
        exp[k] = (np.mean(exp[k]), np.std(exp[k]))

    return exp

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", type="str", dest="inpath", help="=Input List")
    (options, args) = parser.parse_args()
    # print get_cache_hits(zip(*AnalyzeResults.parse(options.inpath)))
    # query, results, complatency, e2elat = get_cache_hits_nodes(options.inpath)
    # print("Precision:{} Recall:{} CompLatency:{} E2ELat:{}".format(AnalyzeResults.precision(query, results),
    #                                                                         AnalyzeResults.recall(query, results),
    #                                                                         AnalyzeResults.avglatency(complatency),
    #                                                                         AnalyzeResults.avglatency(e2elat)))

    pprint(analyze_iters(options.inpath))