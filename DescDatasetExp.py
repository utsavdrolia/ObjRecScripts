import os
import shutil
import sys
from optparse import OptionParser

import numpy as np

from RunPipeline import run_pipeline
from PrecisionRecallAnalysis import precision, recall
import json

EXPERIMENTS_DIR = "/Users/utsav/Documents/DATA/Research/HYRAX/Datasets/ObjectRecog/UMissouri/Experiment"
UMISS_DATASET = "/Users/utsav/Documents/DATA/Research/HYRAX/Datasets/ObjectRecog/UMissouri/Dataset/Database_images/_list_images.txt"
UMISS_QUERIES = "/Users/utsav/Documents/DATA/Research/HYRAX/Datasets/ObjectRecog/UMissouri/Dataset/Query_images/_list_images.txt"
ORB_PARS = "/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/orb_pars.txt"


def run_iter(iter_folder, objects, descnum):
    if os.path.exists(iter_folder):
        shutil.rmtree(iter_folder)
    os.mkdir(iter_folder)
    EXP_DB = iter_folder + os.sep + "DBImages"
    EXP_QUERIES = iter_folder + os.sep + "Queries"
    RESULT = iter_folder + os.sep + "results"
    run_pipeline(UMISS_DATASET, EXP_DB, objects, UMISS_QUERIES, EXP_QUERIES, descnum, ORB_PARS, RESULT)
    q, r = parse_results(RESULT)
    prec = precision(q, r)
    rec = recall(q, r)
    json.dump({"precision": prec, "recall": rec}, open(iter_folder + os.sep + "analysis", "w"))
    return prec, rec


def run_iters(start, stop, objects, descnum):
    exp_dir = EXPERIMENTS_DIR + os.sep + "O_" + str(objects) + os.sep + "D_" + str(descnum)
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)

    precs = []
    recs = []
    for iteration in range(start, stop + 1):
        iter_folder = exp_dir + os.sep + "Iter_" + str(iteration)
        prec, rec = run_iter(iter_folder, objects, descnum)
        precs.append(prec)
        recs.append(rec)

    json.dump({"precision": (np.mean(precs), np.std(precs)), "recall": (np.mean(recs), np.std(recs))}, open(exp_dir + os.sep + "analysis", "w"))


def parse_results(result):
    res = open(result)
    lines = res.readlines()
    q = []
    r = []
    for line in lines:
        line = line.strip()
        chunks = line.split(",")
        q.append(chunks[0])
        r.append(chunks[1])
    return q, r

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--numobjects", type="int", dest="numobjects", help="Number of objects in DB")
    parser.add_option("-d", "--descnum", type="int", dest="descnum", help="Number of Descriptors")
    parser.add_option("-s", "--start", type="int", dest="startiter", help="Start Iteration")
    parser.add_option("-e", "--end", type="int", dest="enditer", help="End iteration")
    (options, args) = parser.parse_args()

    run_iters(options.startiter, options.enditer, options.numobjects, options.descnum)