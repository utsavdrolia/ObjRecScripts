import os
import shutil
import sys
from optparse import OptionParser

import numpy as np

from RunPipelineServer import run_pipeline
from PrecisionRecallAnalysis import precision, recall
import json
from FileSystemGlobals import *

# To run EvaluateServerClient

def run_iter(iter_folder, objects, descnum, featuretype, matchertype_db, matchertype_cache, cachesize):
    if os.path.exists(iter_folder):
        shutil.rmtree(iter_folder)
    os.mkdir(iter_folder)
    EXP_DB = iter_folder + os.sep + "DBImages"
    EXP_QUERIES = iter_folder + os.sep + "Queries"
    RESULT = iter_folder + os.sep + "results"
    run_pipeline(SERVER, UMISS_DATASET, EXP_DB, objects, UMISS_QUERIES, EXP_QUERIES, descnum, RESULT, featuretype, matchertype_db, matchertype_cache, cachesize)
    q, r, t = parse_results(RESULT)
    prec = precision(q, r)
    rec = recall(q, r)
    lat = np.mean(t)
    json.dump({"precision": prec, "recall": rec, "latency": lat}, open(iter_folder + os.sep + "analysis", "w"))
    return prec, rec, lat


def run_iters(start, stop, objects, descnum,featuretype, matchertype_db, matchertype_cache, cachesize):
    exp_dir = EXPERIMENTS_DIR + os.sep + "O_" + str(objects) + os.sep + "D_" + str(cachesize)
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)

    precs = []
    recs = []
    lats = []
    for iteration in range(start, stop + 1):
        print("Running Iteration: {}".format(iteration))
        iter_folder = exp_dir + os.sep + "Iter_" + str(iteration)
        prec, rec, lat = run_iter(iter_folder, objects, descnum, featuretype, matchertype_db, matchertype_cache, cachesize)
        precs.append(prec)
        recs.append(rec)
        lats.append(lat)
    results = {"precision": (np.mean(precs), np.std(precs)), "recall": (np.mean(recs), np.std(recs)),
               "latency": (np.mean(lats), np.std(lats))}
    print(results)
    json.dump(results, open(exp_dir + os.sep + "analysis", "w"))


def parse_results(result):
    res = open(result)
    lines = res.readlines()
    q = []
    r = []
    t =[]
    for line in lines:
        line = line.strip()
        chunks = line.split(",")
        q.append(chunks[0])
        r.append(chunks[1])
        t.append(int(chunks[2]))
    return q, r, t

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--numobjects", type="int", dest="numobjects", help="Number of objects in DB")
    parser.add_option("-d", "--descnum", type="int", dest="descnum", help="Number of Descriptors")
    parser.add_option("-s", "--start", type="int", dest="startiter", help="Start Iteration")
    parser.add_option("-e", "--end", type="int", dest="enditer", help="End iteration")
    (options, args) = parser.parse_args()

    run_iters(options.startiter, options.enditer, options.numobjects, options.descnum)